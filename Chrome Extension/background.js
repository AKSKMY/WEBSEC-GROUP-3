chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.type === "analyzeScripts") {
        fetch("http://192.168.200.132:8000/deobfuscate_scripts", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ scripts: message.scripts })
        })
        .then(response => response.json())
        .then(result => {
            console.log("🖥️ Script Analysis Result:", result);

            let likelihood = result.likelihood;  // Probability score from backend
            if (likelihood > 50) {
                alert(`⚠️ Warning! ${likelihood}% chance this website has a keylogger.`);
            } else {
                console.log(`✅ Safe: Only ${likelihood}% chance of keylogger.`);
            }
        })
        .catch(error => {
            console.error("❌ Error analyzing scripts:", error);
        });

        return true;
    }
});

// 🚀 Ensure `content.js` is injected into every new page load
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
    if (changeInfo.status === "complete" && tab.url && tab.url.startsWith("http")) {
        chrome.scripting.executeScript({
            target: { tabId: tabId },
            files: ["content.js"]
        }, () => {
            if (chrome.runtime.lastError) {
                console.error("⚠️ Failed to inject content.js:", chrome.runtime.lastError.message);
            } else {
                console.log("✅ content.js manually injected into tab:", tab.url);
            }
        });
    }
});

// 🚀 Ensure `content.js` is injected again after extension reload
chrome.runtime.onInstalled.addListener(() => {
    chrome.tabs.query({}, tabs => {
        for (let tab of tabs) {
            if (tab.url && tab.url.startsWith("http")) {
                chrome.scripting.executeScript({
                    target: { tabId: tab.id },
                    files: ["content.js"]
                });
            }
        }
    });
});

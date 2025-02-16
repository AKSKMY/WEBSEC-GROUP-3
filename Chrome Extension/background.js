chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.type === "checkKeylogger") {
        fetch("http://192.168.200.132:8000/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(message.data)
        })
        .then(response => response.json())
        .then(result => {
            console.log("🖥️ Backend Prediction:", result);
            sendResponse({ prediction: result.prediction });
        })
        .catch(error => {
            console.error("❌ Error communicating with backend:", error);
            sendResponse({ error: "Failed to connect to backend." });
        });

        return true; // Keeps the service worker alive for async response
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

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.type === "analyzeScripts") {
        console.log("Received script data for analysis:", message.data);

        fetch("http://192.168.200.132:8000/analyze", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ scripts: message.data })
        })
        .then(response => response.json())
        .then(result => {
            console.log("Received analysis result from backend:", result);
            let likelihood = result.results[0]?.likelihood || 0;

            if (likelihood > 50) {
                alert(`⚠️ Warning! ${likelihood}% chance this website has a keylogger.`);
            }
        })
        .catch(error => {
            console.error("Error analyzing scripts:", error);
        });

        return true;
    }
});

chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
    if (changeInfo.status === "complete" && tab.url && tab.url.startsWith("http")) {
        chrome.scripting.executeScript({
            target: { tabId: tabId },
            files: ["content.js"]
        });
    }
});

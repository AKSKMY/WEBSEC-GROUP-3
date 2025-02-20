const API_URL = "http://20.189.97.207:8000/analyze"; // Ensure this is correct

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.type === "analyzeScripts") {
        console.log("📡 Received script data for analysis:", message.data);

        fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ scripts: message.data })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(result => {
            console.log("✅ Received analysis result from backend:", result);
            
            if (!result.results || result.results.length === 0) {
                console.warn("⚠️ No results received from backend.");
                return;
            }

            let likelihood = result.results[0]?.likelihood || 0;

            if (likelihood > 50) {
                // Send message to content script to show alert
                chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
                    if (tabs.length > 0) {
                        chrome.tabs.sendMessage(tabs[0].id, { type: "showAlert", likelihood });
                    }
                });
            }
        })
        .catch(error => {
            console.error("❌ Error analyzing scripts:", error);
            // Send message to content script for error handling
            chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
                if (tabs.length > 0) {
                    chrome.tabs.sendMessage(tabs[0].id, { type: "showAlert", error: "Failed to analyze scripts. Check console for details." });
                }
            });
        });

        return true; // Ensures async behavior
    }
});

// Inject `content.js` after page loads
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
    if (changeInfo.status === "complete" && tab.url && tab.url.startsWith("http")) {
        console.log(`🔍 Injecting content.js into ${tab.url}`);

        chrome.scripting.executeScript({
            target: { tabId: tabId },
            files: ["content.js"]
        })
        .catch(error => console.error("❌ Failed to inject content script:", error));
    }
});

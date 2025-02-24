const API_URL = "http://20.189.97.207:8000/analyze"; // Ensure this is correct

console.log("✅ Background script is running!");

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    console.log("📩 Received message in background.js:", message);

    if (message.type === "testMessage") {
        console.log("🛠️ Test message received. Sending response...");
        sendResponse({ success: true, message: "Background script is working!" });
        return true;
    }

    if (message.type === "analyzeScripts") {
        console.log("📡 Sending script data for analysis:", JSON.stringify(message.data, null, 2));

        fetch(API_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ scripts: message.data })
        })
        .then(response => response.json())
        .then(result => {
            console.log("✅ Received analysis result from backend:", result);
            let maxLikelihood = Math.max(...result.results.map(r => r.likelihood || 0));
            console.log(`➡️ Max likelihood: ${maxLikelihood}%`);

            if (maxLikelihood > 50) {
                console.warn(`⚠️ High likelihood detected: ${maxLikelihood}%`);

                chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
                    if (tabs.length > 0) {
                        console.log("📩 Sending alert message to content.js in tab:", tabs[0].id);
                        chrome.tabs.sendMessage(tabs[0].id, { 
                            type: "showAlert", 
                            likelihood: maxLikelihood 
                        }, (response) => {
                            if (chrome.runtime.lastError) {
                                console.error("❌ Error sending message to content.js:", chrome.runtime.lastError.message);
                            } else if (response?.success) {
                                console.log("✅ Alert sent successfully.");
                            }
                        });
                    } else {
                        console.warn("⚠️ No active tab found to send alert.");
                    }
                });
            } else {
                console.log("ℹ️ Likelihood too low, no alert sent.");
            }
            sendResponse({ success: true }); // ✅ Ensure response is sent
        })
        .catch(error => {
            console.error("❌ Error analyzing scripts:", error);
            sendResponse({ success: false }); // ✅ Send response on error
        });

        return true; // ✅ Keep message channel open
    }
});

// Inject content.js on page load
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
    if (changeInfo.status === "complete" && tab.url && tab.url.startsWith("http")) {
        console.log(`🔍 Checking injection status for content.js in ${tab.url}`);
        chrome.scripting.executeScript({
            target: { tabId: tabId },
            func: () => !!window.hasInjected
        }, (result) => {
            if (chrome.runtime.lastError) {
                console.error("❌ Failed to check content.js injection status:", chrome.runtime.lastError.message);
                return;
            }
            if (!result || !result[0].result) {
                console.log("🚀 Injecting content.js into:", tab.url);
                chrome.scripting.executeScript({
                    target: { tabId: tabId },
                    files: ["content.js"]
                })
                .then(() => console.log("✅ content.js injected successfully!"))
                .catch(error => console.error("❌ Failed to inject content script:", error));
            } else {
                console.log("✅ content.js is already injected in:", tab.url);
            }
        });
    }
});

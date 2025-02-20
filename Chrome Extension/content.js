console.log("✅ Content script loaded!");

chrome.runtime.sendMessage({ type: "testMessage" }, (response) => {
    console.log("Test response:", response);
});

// Only run once per page.
if (!window.hasInjected) {
    window.hasInjected = true; // Prevent duplicate execution

    function extractAndSendScripts() {
        console.log("🔍 Running extractAndSendScripts...");
        let scripts = document.getElementsByTagName('script');
        let scriptContents = [];

        for (let script of scripts) {
            if (script.src) {
                scriptContents.push({ type: "external", content: script.src });
            } else {
                scriptContents.push({ type: "inline", content: script.innerText });
            }
        }

        if (scriptContents.length > 0) {
            console.log("📜 Extracted scripts:", scriptContents);

            chrome.runtime.sendMessage({ type: "analyzeScripts", data: scriptContents }, (response) => {
                if (chrome.runtime.lastError) {
                    console.error("❌ Message send error:", chrome.runtime.lastError.message);
                } else if (response && response.success) {
                    console.log("✅ Scripts sent successfully");
                }
            });
        }
    }

    // Observe dynamically added scripts.
    const observer = new MutationObserver((mutations) => {
        for (let mutation of mutations) {
            if (mutation.addedNodes) {
                mutation.addedNodes.forEach(node => {
                    if (node.tagName === 'SCRIPT') {
                        console.log("📌 New script detected. Re-scanning...");
                        extractAndSendScripts();
                    }
                });
            }
        }
    });
    observer.observe(document.body, { childList: true, subtree: true });

    // Listen for alert messages from the background script.
    chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
        console.log("📥 Message received in content.js:", message);
        if (message.type === "showAlert") {
            console.log("⚠️ Warning received from background.js:", message.likelihood);
            alert(`⚠️ Warning! ${message.likelihood}% chance this website has a keylogger.`);
            sendResponse({ success: true });
        }
    });

    // Log if running on a local file.
    if (window.location.protocol === "file:") {
        console.log("🔍 Running on a local file (file://)");
    }

    // Trigger extraction once the page fully loads.
    window.addEventListener("load", extractAndSendScripts);
}

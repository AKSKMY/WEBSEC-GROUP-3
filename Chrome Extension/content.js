if (!window.hasInjected) {
    window.hasInjected = true; // Prevent duplicate execution

    function extractAndSendScripts() {
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
            chrome.runtime.sendMessage({ type: "analyzeScripts", data: scriptContents });
        }
    }

    // Observe dynamically added scripts
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

    // Listen for alerts from background.js
    chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
        if (message.type === "showAlert") {
            if (message.likelihood) {
                alert(`⚠️ Warning! ${message.likelihood}% chance this website has a keylogger.`);
            } else if (message.error) {
                alert(`❌ ${message.error}`);
            }
        }
    });

    // Run script extraction after page loads
    window.addEventListener("load", extractAndSendScripts);
}

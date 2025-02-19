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

    console.log("📡 Sending extracted scripts to backend for analysis...");

    chrome.runtime.sendMessage({ type: "analyzeScripts", scripts: scriptContents });
}

extractAndSendScripts();  // Run once on page load

// Re-run when the DOM is updated dynamically (e.g., AJAX calls)
const observer = new MutationObserver(() => {
    extractAndSendScripts();
});
observer.observe(document, { childList: true, subtree: true });

console.log("✅ content.js script extraction is active.");

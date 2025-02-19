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

        console.log("Extracted scripts:", scriptContents);

        chrome.runtime.sendMessage({ type: "analyzeScripts", data: scriptContents });
    }

    // Observe dynamically added scripts
    const observer = new MutationObserver((mutations) => {
        for (let mutation of mutations) {
            if (mutation.addedNodes) {
                mutation.addedNodes.forEach(node => {
                    if (node.tagName === 'SCRIPT') {
                        extractAndSendScripts();
                    }
                });
            }
        }
    });

    observer.observe(document.body, { childList: true, subtree: true });

    window.addEventListener("load", extractAndSendScripts);
}

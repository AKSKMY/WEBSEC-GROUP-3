console.log("Content script loaded!");

// Function to detect potentially malicious scripts
function detectScripts() {
  let maliciousDetected = false;

  // 1. Detect `keydown` event listeners (to identify keyloggers)
  const originalAddEventListener = EventTarget.prototype.addEventListener;
  EventTarget.prototype.addEventListener = function (type, listener, options) {
    if (type === "keydown") {
      console.warn("Keylogger detected: A keydown event listener was added.");
      maliciousDetected = true;

      // Trigger alert page immediately for keylogger detection
      sendAlertMessage();
    }
    return originalAddEventListener.call(this, type, listener, options);
  };

  // 2. Monitor dynamically added scripts using MutationObserver
  const observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
      mutation.addedNodes.forEach((node) => {
        if (node.tagName === "SCRIPT") {
          console.warn("New script dynamically added to the page:", node);
          maliciousDetected = true;
          sendAlertMessage();
        }
      });
    });
  });

  observer.observe(document.documentElement, { childList: true, subtree: true });

  // Trigger the alert if anything malicious is detected
  if (maliciousDetected) {
    sendAlertMessage();
  }
}

// Function to send a message to the background script to trigger the alert page
function sendAlertMessage() {
  chrome.runtime.sendMessage({ action: "showAlertPage" });
}

// Run the detection script on page load
detectScripts();

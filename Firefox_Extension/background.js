chrome.runtime.onMessage.addListener((message, sender) => {
  if (message.action === "showAlertPage") {
    // Redirect the current tab to the alert.html page
    chrome.tabs.update(sender.tab.id, {
      url: chrome.runtime.getURL("warning.html")
    });
  }
});

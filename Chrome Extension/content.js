function sendKeyloggerData(event) {
    const data = {
        key: event.key,
        timestamp: Date.now()
    };

    console.log("📡 Sending data to backend:", data);

    try {
        chrome.runtime.sendMessage(
            { type: "checkKeylogger", data: data },
            response => {
                if (chrome.runtime.lastError) {
                    console.error("❌ Background script unavailable, retrying...");
                    setTimeout(() => sendKeyloggerData(event), 1000); // Retry after 1 second
                    return;
                }

                if (response) {
                    console.log("✅ Response from backend:", response);
                    if (response.prediction === 1) {
                        alert("⚠️ Keylogger Detected! Please be cautious.");
                    }
                } else {
                    console.error("❌ No response from backend.");
                }
            }
        );
    } catch (error) {
        console.error("❌ Extension context invalidated, retrying...");
        setTimeout(() => sendKeyloggerData(event), 1000); // Retry after 1 second
    }
}

// Listen for keypress events and call `sendKeyloggerData`
document.addEventListener("keydown", sendKeyloggerData);

console.log("✅ content.js has been injected successfully.");

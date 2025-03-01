document.addEventListener('DOMContentLoaded', function() {
    // Get the DOM elements for the buttons and content
    const goBackButton = document.getElementById('go-back');
    const proceedButton = document.getElementById('proceed-button');
    const securityAlert = document.getElementById('security-alert');
    const likelihoodText = document.getElementById('likelihood-text');
    const detectionDetails = document.getElementById('detection-details');
    const urlParams = new URLSearchParams(window.location.search);
    const targetUrl = urlParams.get('targetUrl');


    // Assuming maxLikelihood and detection details come from the previous scan result
    let maxLikelihood = 75; // Example likelihood (this should be set dynamically)
    let detailsFound = true; // This flag should be set based on scan results
  
    // Update the security alert text based on likelihood
    if (maxLikelihood > 80) {
      securityAlert.innerHTML = 'Security Alert: High Risk Detected';
      likelihoodText.innerHTML = `We have identified a ${maxLikelihood}% chance of a keylogger on this website. Proceeding could expose your sensitive information.`;
    } else if (maxLikelihood > 50) {
      securityAlert.innerHTML = 'Security Alert: Potential Risk Detected';
      likelihoodText.innerHTML = `This website has a ${maxLikelihood}% chance of containing a keylogger.`;
    } else {
      securityAlert.innerHTML = 'Security Alert: Low Risk Detected';
      likelihoodText.innerHTML = `This website has a ${maxLikelihood}% chance of containing a keylogger.`;
    }
  
    // Add breakdown of suspicious behaviors if found
    if (detailsFound) {
      let detailsHTML = "<li>Detected patterns consistent with keylogging behavior</li>";
      detailsHTML += "<li>Found JavaScript that tracks and records keyboard input</li>";
      detailsHTML += "<li>Identified potential data transmission to external servers</li>";
      detectionDetails.innerHTML = detailsHTML;
    }
  
     // Button event handlers (these are for the current page, will be replaced after redirect)
     proceedButton.addEventListener('click', function() {
        console.log("👍 User chose to proceed to:", targetUrl);
        if (targetUrl) {
            // Signal to background script this URL is approved for one-time bypass
            // AND request direct navigation from the background script
            chrome.runtime.sendMessage({ 
                type: "navigateAfterScan", 
                url: targetUrl 
            }, function(response) {
                console.log("Navigate response:", response);
                
                // Fallback in case background navigation fails
                if (!response || !response.success) {
                    console.log("⚠️ Background navigation failed, trying direct navigation");
                    window.location.href = targetUrl;
                }
            });
        }
    });
    
    goBackButton.addEventListener('click', function() {
        console.log("👎 User chose not to proceed");
        
        // Ask the background script to handle the navigation back
        chrome.runtime.sendMessage({ 
            type: "cancelNavigation"
        }, function(response) {
            console.log("Cancel navigation response:", response);
            
            // Fallback if the background script fails to handle it
           // If the background script successfully handled it, try closing the tab
        if (response && response.success) {
            console.log("✅ Closing warning tab");
            window.close();
        } else {
            console.log("⚠️ Background script failed, redirecting to a fallback page.");
            window.location.href = "chrome://newtab/"; // Change this to a safe fallback page
        }
      });
    });
  });
  
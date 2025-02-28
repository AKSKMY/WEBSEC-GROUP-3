let isActive = true; 
let isPreScanEnabled = false;

// Initialize settings from storage
chrome.storage.local.get(['isActive', 'preScanEnabled'], function(result) {
    if (result.isActive !== undefined) {
        isActive = result.isActive;
        updateStatusDisplay();
    }
    
    if (result.preScanEnabled !== undefined) {
        isPreScanEnabled = result.preScanEnabled;
        updatePreScanDisplay();
    }
});

function toggleDetectionStatus() {
    isActive = !isActive;
    chrome.storage.local.set({isActive: isActive});
    updateStatusDisplay();
}

function togglePreScan() {
    isPreScanEnabled = !isPreScanEnabled;
    chrome.storage.local.set({preScanEnabled: isPreScanEnabled});
    updatePreScanDisplay();
}

function updateStatusDisplay() {
    const statusElement = document.getElementById("status");
    if (isActive) {
        statusElement.textContent = "Active";
        statusElement.className = "status active";
    } else {
        statusElement.textContent = "Inactive";
        statusElement.className = "status inactive";
    }
}

function updatePreScanDisplay() {
    const preScanStatus = document.getElementById("prescan-status");
    if (isPreScanEnabled) {
        preScanStatus.textContent = "Enabled";
        preScanStatus.className = "status active";
    } else {
        preScanStatus.textContent = "Disabled";
        preScanStatus.className = "status disabled";
    }
}

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById("test").addEventListener("click", toggleDetectionStatus);
    document.getElementById("prescan-toggle").addEventListener("click", togglePreScan);
});

let isActive = 1; 

function toggleDetectionStatus() {
    const statusElement = document.getElementById("status");
    if (isActive) {
        statusElement.textContent = "Inactive";  
        statusElement.style.color = "red";   
        alert("Webshield Tool is now inactive."); 
   
    } else {
        statusElement.textContent = "Active";   
        statusElement.style.color = "green"; 
        alert("Webshield Tool is now running."); 
  
    }
    isActive = !isActive; 
}
document.getElementById("test").addEventListener("click", toggleDetectionStatus);

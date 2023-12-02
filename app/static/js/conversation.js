document.addEventListener('DOMContentLoaded', function () {
    fetch('/transcriptions')
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById('conversation');
            data.forEach(item => {
                const div = document.createElement('div');
                div.textContent = `Speaker: ${item.speaker}, Text: ${item.text}`;
                container.appendChild(div);
            });
        })
        .catch(error => console.error('Error:', error));
});

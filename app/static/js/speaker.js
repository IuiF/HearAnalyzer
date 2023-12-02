document.addEventListener('DOMContentLoaded', function () {
    fetch('/transcriptions')
        .then(response => response.json())
        .then(data => {
            const conversationContainer = document.getElementById('conversation');

            data.forEach(item => {
                const messageDiv = document.createElement('div');
                messageDiv.classList.add('message');

                const img = document.createElement('img');
                img.classList.add('speaker-icon');
                img.src = `static/images/${item.speaker}.png`;  // 画像ファイルのパス

                const textSpan = document.createElement('span');
                textSpan.classList.add('speaker-text');
                textSpan.textContent = item.text;

                messageDiv.appendChild(img);
                messageDiv.appendChild(textSpan);

                conversationContainer.appendChild(messageDiv);
            });
        })
        .catch(error => console.error('Error:', error));
});

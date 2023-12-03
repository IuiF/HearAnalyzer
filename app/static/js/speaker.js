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
                img.addEventListener('click', function () {
                    jumpToTime(item.start);
                });

                const textSpan = document.createElement('span');
                textSpan.classList.add('speaker-text');
                textSpan.textContent = item.text;
                textSpan.addEventListener('click', function () {
                    navigator.clipboard.writeText(item.text)
                        .then(() => {
                            console.log('Text copied to clipboard:', item.text);
                            // アニメーションクラスを追加
                            textSpan.classList.add('copied');

                            // 一定時間後にクラスを削除
                            setTimeout(() => {
                                textSpan.classList.remove('copied');
                            }, 500); // .5秒後に削除
                        })
                        .catch(error => {
                            console.error('Error copying text to clipboard:', error);
                        });
                });

                messageDiv.appendChild(img);
                messageDiv.appendChild(textSpan);

                conversationContainer.appendChild(messageDiv);
            });
        })
        .catch(error => console.error('Error:', error));
});

function jumpToTime(time) {
    const player = videojs('my-video');
    player.currentTime(time); // 秒単位で再生位置を設定
    player.play(); // ビデオの再生を開始
}

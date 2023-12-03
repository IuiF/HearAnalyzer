document.addEventListener('DOMContentLoaded', function () {
    // トランスクリプションデータを取得
    fetch('/transcriptions')
        .then(response => response.json())
        .then(data => {
            const conversationContainer = document.getElementById('conversation');

            // トランスクリプション項目を一つずつ処理
            data.forEach(item => {
                const messageDiv = document.createElement('div');
                messageDiv.classList.add('message');
                messageDiv.dataset.start = item.start; // 開始時間のデータ属性を設定
                messageDiv.dataset.end = item.end;     // 終了時間のデータ属性を設定

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

            // Video.jsプレイヤーを取得
            const player = videojs('my-video');

            // 'timeupdate'イベントハンドラーをプレイヤーに追加
            player.on('timeupdate', function () {
                const currentTime = player.currentTime();
                const messages = document.querySelectorAll('.message');

                // 現在の再生時間に最も近いメッセージを探す
                let activeMessage = null;
                messages.forEach(message => {
                    const start = parseFloat(message.dataset.start);
                    const end = parseFloat(message.dataset.end);

                    if (currentTime >= start && currentTime < end) {
                        message.classList.add('active');
                        activeMessage = message;
                    } else {
                        message.classList.remove('active');
                    }
                });

                // アクティブなメッセージがあればスクロール
                if (activeMessage) {
                    const rect = activeMessage.getBoundingClientRect();
                    if (rect.bottom > window.innerHeight || rect.top < 0) {
                        activeMessage.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    }
                }
            });
        })
        .catch(error => console.error('Error:', error));
});

// 指定された時間にジャンプする関数
function jumpToTime(time) {
    const player = videojs('my-video');
    player.currentTime(time); // 秒単位で再生位置を設定
    player.play(); // ビデオの再生を開始
}

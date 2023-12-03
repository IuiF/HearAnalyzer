document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('analyze-form');
    const resultDiv = document.getElementById('result');

    form.addEventListener('submit', function (event) {
        event.preventDefault(); // フォームのデフォルトの送信を防止

        const formData = new FormData(form);
        fetch('/analyze', {
            method: 'POST',
            body: formData
        })
            .then(response => response.json())
            .then(data => {
                // 解析結果をresultDivに表示
                resultDiv.textContent = data.result; // 仮定: バックエンドが {result: '...'} の形式でレスポンスを返す
            })
            .catch(error => {
                console.error('Error:', error);
                resultDiv.textContent = 'エラーが発生しました。';
            });
    });
});

$(document).ready(function () {
    $('#analyze-form').submit(function (e) {
        e.preventDefault();
        var formData = $(this).serialize();

        $.ajax({
            type: "POST",
            url: "/analyze",
            data: formData,
            dataType: "json",
            success: function (response) {
                var highlightedSentence = "";
                response.dependencies.forEach(function (dep, index) {
                    var token = response.tokens[index];
                    var className = "";

                    if (dep.dep === "名詞の主語") {
                        className = "highlight-subject";
                    } else if (dep.dep === "文のルート") {
                        className = "highlight-verb";
                    }

                    if (className) {
                        highlightedSentence += "<span class='" + className + "'>" + token + "</span> ";
                    } else {
                        highlightedSentence += token + " ";
                    }
                });

                var resultHtml = "<div class='sentence'>" + highlightedSentence.trim() + "</div>";
                resultHtml += "<div>(" + response.translated_text + ")</div>";

                $('.result').html(resultHtml);
            },
            error: function () {
                alert('エラーが発生しました。');
            }
        });
    });
});

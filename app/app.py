from flask import Flask, render_template, request
from ..utils.VideoDownloader import VideoDownloader
from ..utils.TextAnalyzer import TextAnalyzer

app = Flask(__name__)

def youtube_analize(url):
    dl = VideoDownloader()
    dl.download_video(video_link=url, output_path='tmp/')


@app.route("/")
def home():
    input = 'world'
    return render_template("upload.html", input = input)

@app.route("/index", methods=['POST'])
def index():
    input2 = request.form['link1']
    return render_template("index.html", input2 = input2)

# @app.route("/tmpp", methods=['POST'])
# def tmp():
#     link1 = request.form['link1']
#     return render_template("tmp.html", link1 = link1)

if __name__ == "__main__":
    app.run(debug=True)

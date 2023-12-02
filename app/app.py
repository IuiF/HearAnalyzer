import sys
import os
sys.path.append(os.pardir)

from flask import Flask, render_template, request
from utils.VideoDownloader import VideoDownloader
from utils.MediaConverter import MediaConverter
from utils.AudioTranscriber import AudioTranscriber
from dotenv import load_dotenv
from utils.TextAnalyzer import TextAnalyzer

app = Flask(__name__)

def generate_script_from_url(url):
    dl = VideoDownloader()
    dl.download_video(video_link=url, output_path='tmp/video.mp4')
    try:
        converter = MediaConverter("tmp/video.mp4")
        output_file = converter.convert()
        print('#########',output_file)
    except ValueError as e:
        print(e)
    # .env ファイルを読み込む
    load_dotenv(".env")

def generate_script_from_file(file):
    try:
        converter = MediaConverter(file)
        output_file = converter.convert()
        print('#########',output_file)
    except ValueError as e:
        print(e)
    # .env ファイルを読み込む
    load_dotenv(".env")

    # 使用例
    transcriber = AudioTranscriber(
        input_path="tmp/video.mp3",
        db_path="tmp/output.db",
        model_name="large-v3",  # モデルのサイズによっては 'small', 'medium', 'large', 'base', 'large-v3' などを選択
        token_key=os.getenv("HuggingFace_Taken"),
        gcp_path=os.getenv("GCPKey_Path"),
    )
    transcriber.process()


@app.route("/")
def home():
    input = 'world'
    return render_template("upload.html", input = input)

@app.route("/index", methods=['POST'])
def index():
    key = list(request.form.keys())[0]
    if key == 'link1':
        input2 = request.form[key]
        generate_script_from_url(input2)
    elif key == 'file1':
        input2 = request.form[key]
        generate_script_from_file(input2)
    return render_template("index.html", input2 = input2)

# @app.route("/tmpp", methods=['POST'])
# def tmp():
#     link1 = request.form['link1']
#     return render_template("tmp.html", link1 = link1)

if __name__ == "__main__":
    app.run(debug=True)

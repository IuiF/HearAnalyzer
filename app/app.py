import sys
import os

sys.path.append(os.pardir)

from flask import Flask, render_template, request, jsonify
from utils.VideoDownloader import VideoDownloader
from utils.MediaConverter import MediaConverter
from utils.AudioTranscriber import AudioTranscriber
from dotenv import load_dotenv
from utils.TextAnalyzer import TextAnalyzer
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
load_dotenv(".env")


def generate_script_from_url(url):
    dl = VideoDownloader()
    dl.download_video(video_link=url, output_path="app/static/tmp/video.mp4")
    try:
        converter = MediaConverter("app/static/tmp/video.mp4")
        output_file = converter.convert()
        # print("#########", output_file)
    except ValueError as e:
        print(e)

    # 使用例
    transcriber = AudioTranscriber(
        input_path="app/static/tmp/video.mp3",
        db_path="app/static/tmp/output.db",
        model_name="large-v3",  # モデルのサイズによっては 'small', 'medium', 'large', 'base', 'large-v3' などを選択
        token_key=os.getenv("HuggingFace_Taken"),
        gcp_path=os.getenv("GCPKey_Path"),
    )
    transcriber.process()


def generate_script_from_file(file):
    try:
        converter = MediaConverter(file, output_path="app/static/tmp")
        output_file = converter.convert()
        print("#########", output_file)
    except ValueError as e:
        print(e)

    # 使用例
    transcriber = AudioTranscriber(
        input_path="app/static/tmp/video.mp3",
        db_path="app/static/tmp/output.db",
        model_name="large-v3",  # モデルのサイズによっては 'small', 'medium', 'large', 'base', 'large-v3' などを選択
        token_key=os.getenv("HuggingFace_Taken"),
        gcp_path=os.getenv("GCPKey_Path"),
    )
    transcriber.process()


db_path = "app/static/tmp/output.db"
db_uri = "sqlite:///{}".format(os.path.abspath(db_path))
app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Transcription(db.Model):
    __tablename__ = "transcriptions"

    id = db.Column(db.Integer, primary_key=True)
    start = db.Column(db.Float, nullable=False)
    end = db.Column(db.Float, nullable=False)
    speaker = db.Column(db.String, nullable=True)
    text = db.Column(db.String, nullable=False)
    translation = db.Column(db.String, nullable=True)


class AudioSegment(db.Model):
    __tablename__ = "audio_segments"

    id = db.Column(db.Integer, primary_key=True)
    audio = db.Column(db.LargeBinary, nullable=False)


def get_translation(transcription_id):
    transcription = Transcription.query.get(transcription_id)
    if transcription:
        return transcription.translation
    else:
        return None


@app.route("/")
def upload():
    input = "world"
    return render_template("upload.html", input=input)


@app.route("/index", methods=["POST"])
def index():
    key = list(request.form.keys())[0]
    if key == "link1":
        input2 = request.form[key]
        generate_script_from_url(input2)
    elif key == "file1":
        input2 = request.form[key]
        generate_script_from_file(input2)
    return render_template("test.html", input2=input2)


@app.route("/transcriptions")  # 会話情報
def get_transcriptions():
    transcriptions = Transcription.query.all()
    transcription_data = [
        {
            "speaker": transcription.speaker,
            "text": transcription.text,
            "translation": transcription.translation,
        }
        for transcription in transcriptions
    ]
    return jsonify(transcription_data)


@app.route("/test")
def test():
    return render_template("test.html")


if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)


db_path = "app/tmp/output.db"
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
    return render_template("upload.html")


@app.route("/index")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)

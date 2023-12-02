import os
import tempfile
from pydub import AudioSegment
import whisper
import torch
from pyannote.audio import Pipeline
import sqlite3
import six
from google.cloud import translate_v2 as translate


def create_database(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # トランスクリプションを保存するテーブル
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS transcriptions (
            id INTEGER PRIMARY KEY,
            start REAL,
            end REAL,
            speaker TEXT,
            text TEXT,
            translation TEXT
        )
    """
    )

    # 音声セグメントを保存するテーブル
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS audio_segments (
            id INTEGER PRIMARY KEY,
            audio BLOB
        )
    """
    )

    conn.commit()
    conn.close()


class AudioTranscriber:
    def __init__(
        self,
        input_path=None,
        db_path="tmp_transcription.db",
        model_name="base",
        token_key=None,
        gcp_path=None,
    ):
        self.input_path = input_path
        self.db_path = db_path
        self.model_name = model_name
        self.token_key = token_key

        # DBが既に存在する場合は削除
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        create_database(self.db_path)

        self.gcp_path = gcp_path
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.gcp_path

    def process(self):
        # モデルのロード
        pipeline = Pipeline.from_pretrained(
            "pyannote/speaker-diarization-3.1", use_auth_token=self.token_key
        )
        pipeline = pipeline.to(torch.device("cuda"))
        model = whisper.load_model(self.model_name)

        # 話者分離
        diarization = pipeline(self.input_path)

        # データベース接続
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # 各セグメントの処理
        for segment, _, speaker in diarization.itertracks(yield_label=True):
            start_ms = int(segment.start * 1000)
            end_ms = int(segment.end * 1000)
            audio = AudioSegment.from_file(self.input_path)[start_ms:end_ms]

            # 一時ファイルにセグメントを保存
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
                audio.export(tmp_file.name, format="wav")
                tmp_file_path = tmp_file.name

            # 一時ファイルから文字起こしを行う
            text_en = model.transcribe(tmp_file_path)["text"]
            if isinstance(text_en, six.binary_type):
                text_en = text_en.decode("utf-8")

            # Translate Clientの生成
            translate_client = translate.Client()

            # 英語テキストを日本語に翻訳
            translation = translate_client.translate(text_en, target_language="ja")
            translated_text = translation["translatedText"]

            # トランスクリプションをデータベースに保存
            cursor.execute(
                """
                INSERT INTO transcriptions (start, end, speaker, text, translation)
                VALUES (?, ?, ?, ?, ?)
            """,
                (segment.start, segment.end, speaker, text_en, translated_text),
            )

            # 音声セグメントをデータベースに保存
            with open(tmp_file_path, "rb") as audio_file:
                audio_data = audio_file.read()
                cursor.execute(
                    """
                    INSERT INTO audio_segments (audio)
                    VALUES (?)
                """,
                    (audio_data,),
                )

            # 一時ファイルを削除
            os.remove(tmp_file_path)

        # 変更をコミットし、接続を閉じる
        conn.commit()
        conn.close()

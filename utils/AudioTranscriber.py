import os
import tempfile
import csv
from pydub import AudioSegment
import whisper
import torch
from pyannote.audio import Pipeline
import sqlite3


def create_database(db_path):
    # 既に存在する場合は削除
    if os.path.exists(db_path):
        os.remove(db_path)

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
            text TEXT
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
    ):
        self.input_path = input_path
        self.db_path = db_path
        self.model_name = model_name
        self.token_key = token_key
        create_database(self.db_path)

    def process(self):
        # モデルのロード
        pipeline = Pipeline.from_pretrained(
            "pyannote/speaker-diarization", use_auth_token=self.token_key
        )
        pipeline = pipeline.to(torch.device("cuda"))
        model = whisper.load_model(self.model_name)

        # 話者分離
        diarization = pipeline(self.input_path)

        # データベース接続
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # 結果をCSVファイルに書き込む準備
        with open(self.output_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Start", "End", "Speaker", "Text"])

            # 各セグメントの処理
            for segment, _, speaker in diarization.itertracks(yield_label=True):
                start_ms = int(segment.start * 1000)
                end_ms = int(segment.end * 1000)
                audio = AudioSegment.from_file(self.input_path)[start_ms:end_ms]

                # 一時ファイルにセグメントを保存
                with tempfile.NamedTemporaryFile(
                    suffix=".wav", delete=False
                ) as tmp_file:
                    audio.export(tmp_file.name, format="wav")
                    tmp_file_path = tmp_file.name

                # 一時ファイルから文字起こしを行う
                text = model.transcribe(tmp_file_path)["text"]
                # print(
                #     f'[{segment.start:03.1f}s - {segment.end:03.1f}s] {speaker}: {text}'
                # )

                # トランスクリプションをデータベースに保存
                cursor.execute(
                    """
                    INSERT INTO transcriptions (start, end, speaker, text)
                    VALUES (?, ?, ?, ?)
                """,
                    (segment.start, segment.end, speaker, text),
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

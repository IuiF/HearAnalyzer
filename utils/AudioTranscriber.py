import os
import tempfile
import csv
from pydub import AudioSegment
import whisper
import torch
from pyannote.audio import Pipeline


class AudioTranscriber:
    def __init__(
        self, input_path=None, output_path=None, model_name="base", token_key=None
    ):
        self.input_path = input_path
        self.output_path = output_path or "transcription.csv"
        self.model_name = model_name
        self.token_key = token_key

    def process(self):
        # モデルのロード
        pipeline = Pipeline.from_pretrained(
            "pyannote/speaker-diarization", use_auth_token=self.token_key
        )
        pipeline = pipeline.to(torch.device("cuda"))
        model = whisper.load_model(self.model_name)

        # 話者分離
        diarization = pipeline(self.input_path)

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

                # CSVファイルに書き込み
                quoted_text = f'"{text}"'
                writer.writerow([segment.start, segment.end, speaker, quoted_text])

                # 一時ファイルを削除
                os.remove(tmp_file_path)

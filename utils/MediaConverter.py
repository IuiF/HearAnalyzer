from moviepy.editor import VideoFileClip
from pydub import AudioSegment
import os


class MediaConverter:
    MAX_DURATION_SECONDS = 20 * 60  # 20 minutes
    BITRATE = "128k"  # 128 kbps

    def __init__(self, file_path):
        self.file_path = file_path
        self.extension = os.path.splitext(file_path)[1].lower()

    def convert(self):
        supported_formats = [".mp4", ".mkv", ".avi", ".mp3", ".mpga", ".m4a", ".wav"]

        if self.extension not in supported_formats:
            raise ValueError(
                f"予期されていないファイル形式のようです\nアップロードしたファイル形式:{self.extension.replace('.','')}"
            )

        if not self.is_duration_valid():
            raise ValueError("メディアが20分を超えています")

        if self.extension in [".mp4", ".mkv", ".avi"]:  # 動画を音声ファイルに変換
            return self.extract_audio_from_video()

        elif self.extension in [".mp3", ".mpga", ".m4a", ".wav"]:
            return self.convert_audio_to_mp3()  # MP3に変換

    def extract_audio_from_video(self):  # 動画を音声に変換
        output_path = os.path.splitext(self.file_path)[0] + ".mp3"
        video_clip = VideoFileClip(self.file_path)
        video_clip.audio.write_audiofile(output_path, bitrate=self.BITRATE)
        return output_path

    def convert_audio_to_mp3(self):  # 音声をmp3に変換
        output_path = os.path.splitext(self.file_path)[0] + ".mp3"
        audio = AudioSegment.from_file(self.file_path)
        audio.export(output_path, format="mp3", bitrate=self.BITRATE)
        return output_path

    def is_duration_valid(self):  # メディアファイルの長さを確認
        if self.extension in [".mp4", ".mkv", ".avi"]:
            video = VideoFileClip(self.file_path)
            return video.duration <= MediaConverter.MAX_DURATION_SECONDS
        else:
            audio = AudioSegment.from_file(self.file_path)
            return len(audio) <= MediaConverter.MAX_DURATION_SECONDS * 1000

from moviepy.editor import VideoFileClip
from pydub import AudioSegment
import os


class MediaConverter:
    MAX_DURATION_SECONDS = 60 * 60  # 60 minutes
    BITRATE = "128k"  # 128 kbps

    def __init__(self, file_path, output_path):
        self.file_path = file_path
        self.output_path = output_path
        self.extension = os.path.splitext(file_path)[1].lower()

    def convert(self):
        supported_formats = [".mp4", ".mkv", ".avi", ".mp3", ".mpga", ".m4a", ".wav"]

        if self.extension not in supported_formats:
            raise ValueError(
                f"予期されていないファイル形式のようです\nアップロードしたファイル形式:{self.extension.replace('.','')}"
            )

        if not self.is_duration_valid():
            raise ValueError("メディアが60分を超えています")

        if self.extension in [".mp4", ".mkv", ".avi"]:  # 動画を音声ファイルに変換
            return self.extract_audio_from_video()

        elif self.extension in [".mp3", ".mpga", ".m4a", ".wav"]:
            return self.convert_audio_to_mp3()  # MP3に変換

    def extract_audio_from_video(self):  # 動画を音声に変換
        video_output_path = os.path.join(self.output_path, "video.mp4")
        audio_output_path = os.path.join(self.output_path, "video.mp3")

        video_clip = VideoFileClip(self.file_path)
        video_clip.write_videofile(video_output_path)  # 動画をoutput_path/video.mp4に保存

        audio_clip = video_clip.audio
        temp_path = os.path.splitext(video_output_path)[0] + "_temp.wav"
        audio_clip.write_audiofile(temp_path)
        audio = AudioSegment.from_file(temp_path)  # モノラルに変換
        mono_audio = audio.set_channels(1)
        mono_audio.export(audio_output_path, format="mp3", bitrate=self.BITRATE)
        os.remove(temp_path)  # 一時ファイルを削除

        return audio_output_path

    def convert_audio_to_mp3(self):  # 音声をmp3に変換
        output_path = os.path.join(self.output_path, "video.mp3")
        audio = AudioSegment.from_file(self.file_path)
        audio = audio.set_channels(1)  # モノラル化
        audio.export(output_path, format="mp3", bitrate=self.BITRATE)
        return output_path

    def is_duration_valid(self):  # メディアファイルの長さを確認
        if self.extension in [".mp4", ".mkv", ".avi"]:
            video = VideoFileClip(self.file_path)
            return video.duration <= MediaConverter.MAX_DURATION_SECONDS
        else:
            audio = AudioSegment.from_file(self.file_path)
            return len(audio) <= MediaConverter.MAX_DURATION_SECONDS * 1000

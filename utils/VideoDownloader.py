from yt_dlp import YoutubeDL


class VideoDownloader:
    def __init__(self):
        self.video_link = None
        self.output_path = "../tmp/video.mp4"

    def download_video(self, video_link=None, output_path=None):
        if video_link is not None:
            self.video_link = video_link
        if output_path is not None:
            self.output_path = output_path

        ydl_opts = {
            "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
            "outtmpl": self.output_path,
        }

        ydl = YoutubeDL(ydl_opts)
        ydl.download([self.video_link])

# hackathon2023_12


## 英語スクリプト表示アプリ
- 苦手問題表示






## ffmpegをシステムにインストールする必要があります

### windows
```
$ scoop install ffmpeg
$ choco install ffmpeg
```
### macOS
```
$ brew install ffmpeg
```
### Ubuntu/Debian
```
$ sudo apt-get update
$ sudo apt-get install ffmpeg
```


## pyannote/speaker-diarization と pyannote/segmentation を使用しています

### 以下の規約に同意した上で AccessToken を用意してください

pyannote/speaker-diarization-3.1

[pyannote/speaker-diarization](https://huggingface.co/pyannote/speaker-diarization)

[pyannote/segmentation](https://huggingface.co/pyannote/segmentation)

## GCP Translation API を使用しています
### サービスアカウントキーをJSONファイルを任意のディレクトリに配置してから.envを書き換えてください

[GCP Translation](https://cloud.google.com/translate/?hl=ja)


import os
from pytube import YouTube
from pytube.cli import on_progress
import subprocess


def download_audio(url, start_time=None, end_time=None):
    yt = YouTube(url, on_progress_callback=on_progress)
    stream = yt.streams.filter(only_audio=True).first()

    if not os.path.exists("audio"):
        os.makedirs("audio")

    # Download audio stream
    output_file = stream.download(output_path="audio")

    if start_time is not None and end_time is not None:
        command = (
            f"ffmpeg -i {output_file} -ab 160k -ac 2 -ar 44100 -vn {remove_file_extension(output_file)}.wav"
        )
    else:
        command = f"ffmpeg -i {output_file} -ab 160k -ac 2 -ar 44100 -vn {remove_file_extension(output_file)}.wav"

    subprocess.call(command, shell=True)


def remove_file_extension(file_path):
    return os.path.splitext(file_path)[0]


if __name__ == "__main__":
    url = input("Enter YouTube URL: ")

    download_audio(url)

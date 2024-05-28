import os
import re
from pytube import YouTube, Playlist
from pytube.cli import on_progress
import subprocess


def download_audio_from_video(url, output_folder="audio"):
    yt = YouTube(url, on_progress_callback=on_progress)
    stream = yt.streams.filter(only_audio=True).first()

    if not os.path.exists("audio"):
        os.makedirs("audio")

    # Download audio stream
    output_file = stream.download(output_path=output_folder)
    print(f"Audio downloaded to {output_file}")

    # Convert audio stream to WAV format
    output_wav = remove_file_extension(output_file) + ".wav"
    command = f"ffmpeg -i \"{output_file}\" -ab 160k -ac 2 -ar 44100 -vn \"{output_wav}\""
    subprocess.call(command, shell=True)

    # Clean up the original downloaded file
    os.remove(output_file)
    print(f"Audio converted to WAV format and saved as {output_wav}")


def download_audio_from_playlist(url):
    playlist = Playlist(url)
    special_chars = r'[\\/:*?"<>|]'
    title = playlist.title.strip().replace(" ", "_")
    cleaned_path = re.sub(special_chars, '', title)

    if not os.path.exists(f"audio/{cleaned_path}"):
        os.makedirs(f"audio/{cleaned_path}")

    for video_url in playlist.video_urls:
        print(f"Downloading audio from {video_url}")
        download_audio_from_video(video_url, f"audio/{cleaned_path}")


def remove_file_extension(file_path):
    return os.path.splitext(file_path)[0]


if __name__ == "__main__":
    url = input("Enter YouTube URL (video or playlist, playlists URL must have 'playlist' in the URL to work): ")

    if 'playlist' in url:
        download_audio_from_playlist(url)
    else:
        download_audio_from_video(url)

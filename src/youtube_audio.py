import os
import re
from pytube import YouTube, Playlist
from pytube.cli import on_progress
import spotify_dl
import subprocess
import tkinter as tk
from tkinter import filedialog
import colorama
from colorama import Fore, Style
import torch


# Colored prints setup
def print_colored(text, color):
    colorama.init()
    print(f"{color}{text}{Style.RESET_ALL}")


print_colored(f"GPU (CUDA) Available: {torch.cuda.is_available()}", Fore.CYAN)


def download_audio_from_video(url, output_folder="audio", format="mp3"):
    yt = YouTube(url, on_progress_callback=on_progress)
    stream = yt.streams.filter(only_audio=True).first()

    if not os.path.exists("audio"):
        os.makedirs("audio")

    # Download audio stream
    output_file = stream.download(output_path=output_folder)
    print_colored(f"Audio downloaded to {output_file}\n", Fore.GREEN)

    # Convert audio stream to WAV format
    convert_audio(output_file, output_file, format)


def convert_audio(input_file, output_file, format="mp3"):
    # Convert audio stream to WAV format
    output = remove_file_extension(output_file) + f".{format}"
    command = f'ffmpeg -i "{output_file}" -ab 160k -ac 2 -ar 44100 -vn "{output}"'
    subprocess.call(command, shell=True)

    # Clean up the original downloaded file
    os.remove(output_file)
    print_colored(
        f"Audio converted to {format} format and saved as {output}", Fore.GREEN
    )

    sept = input("Separate instruments? [y/n] ")

    if sept == "y":
        separate_instruments(output)
        print_colored("Instruments separated successfully.", Fore.GREEN)
    else:
        print_colored("Instruments not separated.", Fore.YELLOW)


def download_audio_from_playlist(url):
    playlist = Playlist(url)
    special_chars = r'[\\/:*?"<>|]'
    title = playlist.title.strip().replace(" ", "_")
    cleaned_path = re.sub(special_chars, "", title)

    if not os.path.exists(f"audio/{cleaned_path}"):
        os.makedirs(f"audio/{cleaned_path}")

    for video_url in playlist.video_urls:
        print_colored(f"Downloading audio from {video_url}", Fore.BLUE)
        download_audio_from_video(video_url, f"audio/{cleaned_path}")


def download_audio_from_spotify(url):
    try:
        audio = spotify_dl.download(url)
        convert_audio(audio, audio)
        print_colored(f"Audio downloaded to {audio}\n", Fore.GREEN)
    except Exception as e:
        print_colored(f"An error occurred: {e}, skipping", Fore.RED)


def remove_file_extension(file_path):
    return os.path.splitext(file_path)[0]


def open_file_explorer(path):
    root = tk.Tk()
    root.withdraw()  # Hide the main tkinter window
    file_path = filedialog.askopenfilename()
    print(f"Selected file: {file_path}")
    return file_path


def separate_instruments(file_path, device="cpu"):
    dmcs_comand = f"demucs -d {device} tracks \"{file_path}\""
    print(dmcs_comand)
    subprocess.run(dmcs_comand, shell=True)  # Run the demucs command
    subprocess.run(["explorer separated"])  # Open the "separated" folder


if __name__ == "__main__":

    while True:
        url = input(
            "Enter YouTube URL (video or playlist, playlists URL must have 'playlist' in the URL to work): [q to quit]\n"
        )
        format = input("Enter format for conversion (mp3 or wav): ")

        if url.lower() == "q":
            print_colored("Exiting...", Fore.RED)
            break

        if "spotify" in url:
            download_audio_from_spotify(url)
            continue

        if "playlist" in url:
            download_audio_from_playlist(url, format)
        else:
            download_audio_from_video(url, format=format)

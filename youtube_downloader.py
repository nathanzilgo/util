import tkinter as tk
from tkinter import filedialog, messagebox
from pytube import YouTube


def download_media():
    video_url = url_entry.get()
    output_path = output_path_var.get()
    selected_quality = quality_var.get()
    is_video = media_type_var.get() == "Video"

    try:
        # Create a YouTube object for the given video URL
        yt = YouTube(video_url)

        if is_video:
            # Get the selected video stream
            stream = yt.streams.filter(progressive=True, file_extension="mp4", res=selected_quality).first()
        else:
            # Get the selected audio stream
            stream = yt.streams.filter(only_audio=True, file_extension="mp4").first()

        # Download the media to the specified output path
        stream.download(output_path)

        status_label.config(text="Media downloaded successfully.", fg="green")
    except Exception as e:
        status_label.config(text=f"Error downloading media: {e}", fg="red")


def select_output_path():
    selected_path = filedialog.askdirectory()
    output_path_var.set(selected_path)


# Create the main window
root = tk.Tk()
root.title("YouTube Media Downloader")

# Create and pack widgets
url_label = tk.Label(root, text="Enter YouTube Video URL:")
url_label.grid(row=0, column=0, sticky="w")

url_entry = tk.Entry(root, width=50)
url_entry.grid(row=0, column=1, columnspan=2, padx=5, pady=5)

output_path_label = tk.Label(root, text="Select Output Path:")
output_path_label.grid(row=1, column=0, sticky="w")

output_path_var = tk.StringVar()
output_path_entry = tk.Entry(root, textvariable=output_path_var, width=50)
output_path_entry.grid(row=1, column=1, padx=5, pady=5)

select_path_button = tk.Button(root, text="Select Path", command=select_output_path)
select_path_button.grid(row=1, column=2, padx=5, pady=5)

quality_label = tk.Label(root, text="Select Quality:")
quality_label.grid(row=2, column=0, sticky="w")

quality_var = tk.StringVar()
quality_var.set("720p")
quality_menu = tk.OptionMenu(root, quality_var, "144p", "240p", "360p", "480p", "720p", "1080p")
quality_menu.grid(row=2, column=1, padx=5, pady=5)

media_type_label = tk.Label(root, text="Select Media Type:")
media_type_label.grid(row=3, column=0, sticky="w")

media_type_var = tk.StringVar()
media_type_var.set("Video")
media_type_menu = tk.OptionMenu(root, media_type_var, "Video", "Audio")
media_type_menu.grid(row=3, column=1, padx=5, pady=5)

download_button = tk.Button(root, text="Download Media", command=download_media)
download_button.grid(row=4, column=1, padx=5, pady=5)

status_label = tk.Label(root, text="")
status_label.grid(row=5, column=0, columnspan=3, padx=5, pady=5)

# Start the main event loop
root.mainloop()

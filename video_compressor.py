import tkinter as tk
from tkinter import filedialog, messagebox
from moviepy.editor import VideoFileClip
import os
import subprocess


def compress_video():
    # Get input video file path
    input_file_path = filedialog.askopenfilename(
        filetypes=[("Video files", "*.mp4;*.avi;*.mov")]
    )
    if not input_file_path:
        return  # User canceled or closed the dialog

    # Get output directory path
    output_directory = filedialog.askdirectory()
    if not output_directory:
        return  # User canceled or closed the dialog

    # Get compression quality
    compression_quality = quality_var.get()

    try:
        # Load video clip
        video_clip = VideoFileClip(input_file_path)

        input_filename = os.path.basename(input_file_path)
        output_filename = os.path.join(output_directory, f"{input_filename}_compressed.mp4")

        # Compress the video
        video_clip.write_videofile(
            output_filename,
            codec="libx264",  # Video codec for compression
            preset="medium",  # Compression preset (e.g., ultrafast, superfast, faster, medium, slow)
            bitrate=f"{compression_quality}k",
            audio_codec="aac",
            threads=4,  # Number of threads for video compression
        )

        # Show success message
        messagebox.showinfo(
            "Compression Complete", "Video compression completed successfully."
        )
        # After video compression is complete
        subprocess.Popen(['explorer', output_filename])
    except Exception as e:
        messagebox.showerror("Compression Error", f"Error compressing video: {e}")


# Create the main window
root = tk.Tk()
root.title("Video Compressor")

# Create and pack widgets
select_file_button = tk.Button(root, text="Select Video File", command=compress_video)
select_file_button.pack(padx=10, pady=5)

quality_label = tk.Label(root, text="Select Compression Quality (kbps):")
quality_label.pack(pady=5)

quality_var = tk.IntVar()
quality_var.set(1000)  # Default quality (1000 kbps)
quality_scale = tk.Scale(
    root, from_=50, to=5000, orient=tk.HORIZONTAL, variable=quality_var
)
quality_scale.pack(pady=5)

# Start the main event loop
root.mainloop()

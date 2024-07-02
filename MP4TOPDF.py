import sys
import os
import tempfile
import re
from fpdf import FPDF
from PIL import Image
import cv2
from skimage.metrics import structural_similarity as compare_ssim
import tkinter as tk
from tkinter import filedialog
from tkinter import filedialog, messagebox


def extract_unique_frames(video_file, output_folder, n=3, ssim_threshold=0.8):
    cap = cv2.VideoCapture(video_file)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    last_frame = None
    saved_frame = None
    frame_number = 0
    last_saved_frame_number = -1
    timestamps = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if frame_number % n == 0:
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray_frame = cv2.resize(gray_frame, (128, 72))

            if last_frame is not None:
                similarity = compare_ssim(gray_frame, last_frame, data_range=gray_frame.max() - gray_frame.min())

                if similarity < ssim_threshold:
                    if saved_frame is not None and frame_number - last_saved_frame_number > fps:
                        frame_path = os.path.join(output_folder, f'frame{frame_number:04d}_{frame_number // fps}.png')
                        cv2.imwrite(frame_path, saved_frame)
                        timestamps.append((frame_number, frame_number // fps))

                    saved_frame = frame
                    last_saved_frame_number = frame_number
                else:
                    saved_frame = frame

            else:
                frame_path = os.path.join(output_folder, f'frame{frame_number:04d}_{frame_number // fps}.png')
                cv2.imwrite(frame_path, frame)
                timestamps.append((frame_number, frame_number // fps))
                last_saved_frame_number = frame_number

            last_frame = gray_frame

        frame_number += 1

    cap.release()
    return timestamps

def convert_frames_to_pdf(input_folder, output_file, timestamps):
    frame_files = sorted(os.listdir(input_folder), key=lambda x: int(x.split('_')[0].split('frame')[-1]))
    pdf = FPDF("L")
    pdf.set_auto_page_break(0)

    for i, (frame_file, (frame_number, timestamp_seconds)) in enumerate(zip(frame_files, timestamps)):
        frame_path = os.path.join(input_folder, frame_file)
        image = Image.open(frame_path)
        pdf.add_page()
        pdf.image(frame_path, x=0, y=0, w=pdf.w, h=pdf.h)

        timestamp = f"{timestamp_seconds // 3600:02d}:{(timestamp_seconds % 3600) // 60:02d}:{timestamp_seconds % 60:02d}"

        x, y, width, height = 5, 5, 60, 15
        region = image.crop((x, y, x + width, y + height)).convert("L")
        mean_pixel_value = region.resize((1, 1)).getpixel((0, 0))
        if mean_pixel_value < 64:
            pdf.set_text_color(255, 255, 255)
        else:
            pdf.set_text_color(0, 0, 0)

        pdf.set_xy(x, y)
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 0, timestamp)
    pdf.output(output_file)

def select_video_file():
    file_paths = filedialog.askopenfilenames(filetypes=[("MP4 files", "*.mp4")])
    if file_paths:
        video_entry.delete("1.0", tk.END)  # Clear the entire content of the Text widget
        for file_path in file_paths:
            video_entry.insert(tk.END, file_path + "\n")


def process_video():
    video_files = video_entry.get("1.0", tk.END).strip().split("\n")
    for video_file in video_files:
        if video_file:
            video_file = video_file.strip()
            video_title = os.path.splitext(os.path.basename(video_file))[0]
            output_pdf_filename = f"{video_title}.pdf"

            with tempfile.TemporaryDirectory() as tmp_dir:
                frames_folder = os.path.join(tmp_dir, "frames")
                os.makedirs(frames_folder)

                timestamps = extract_unique_frames(video_file, frames_folder)
                convert_frames_to_pdf(frames_folder, output_pdf_filename, timestamps)
    messagebox.showinfo("Success", "Video conversion to PDF completed successfully!")

# Create the main application window
root = tk.Tk()
root.title("Video to PDF Converter")

video_entry = tk.Text(root ,width=100, height=4)
video_entry.pack(pady=10)

browse_button = tk.Button(root, text="Browse", command=select_video_file)
browse_button.pack(pady=10)

# Create a button to start processing the video
process_button = tk.Button(root, text="Convert to PDF", command=process_video)
process_button.pack(pady=20)

# Start the GUI application
root.mainloop()
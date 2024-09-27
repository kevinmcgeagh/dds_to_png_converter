import os
import time
import subprocess
import shutil  # Import shutil to check for texconv
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import numpy as np
import imageio
import cv2
import pygame

# Global variable to track start time
start_time = None


def convert_dds_to_png_pillow(input_path, output_path):
    try:
        image = Image.open(input_path)
        # Convert the image to 16-bit PNG using numpy
        image_array = np.array(image).astype('uint16')
        converted_image = Image.fromarray(image_array)
        converted_image.save(output_path, format='PNG')
        return converted_image
    except Exception as e:
        log_message(f"Pillow failed to convert {input_path}: {e}")
        return None


def convert_dds_to_png_imageio(input_path, output_path):
    try:
        image = imageio.imread(input_path, format='DDS-FI')
        # Convert to 16-bit and save
        image_array = np.array(image).astype('uint16')
        imageio.imwrite(output_path, image_array, format='PNG')
        return Image.fromarray(image_array)
    except Exception as e:
        log_message(f"ImageIO failed to convert {input_path}: {e}")
        return None


def convert_dds_to_png_opencv(input_path, output_path):
    try:
        image = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
        if image is None:
            raise ValueError("OpenCV failed to load image.")
        # Convert to 16-bit PNG and save
        image_16bit = (image.astype('uint16') * 257) if image.dtype == 'uint8' else image.astype('uint16')
        cv2.imwrite(output_path, image_16bit)
        return Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    except Exception as e:
        log_message(f"OpenCV failed to convert {input_path}: {e}")
        return None


def convert_dds_to_png_pygame(input_path, output_path):
    try:
        pygame.init()
        image = pygame.image.load(input_path)
        pygame.image.save(image, output_path)
        image = Image.open(output_path)
        return image
    except Exception as e:
        log_message(f"PyGame failed to convert {input_path}: {e}")
        return None


def convert_dds_to_png_directxtex(input_path, output_path):
    try:
        # Check if texconv is in the system PATH
        if not shutil.which("texconv"):
            raise EnvironmentError("texconv.exe not found in PATH. Please install DirectXTex and add it to your PATH.")

        # Call DirectXTex via command line
        result = subprocess.run(
            ["texconv", "-ft", "PNG", "-o", os.path.dirname(output_path), input_path],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        if result.returncode == 0:
            converted_image = Image.open(output_path)
            return converted_image
        else:
            raise ValueError("DirectXTex failed with non-zero exit code.")
    except Exception as e:
        log_message(f"DirectXTex failed to convert {input_path}: {e}")
        return None


def convert_dds_to_png(input_path, output_path):
    # Try converting with Pillow first
    converted_image = convert_dds_to_png_pillow(input_path, output_path)
    if converted_image:
        return converted_image

    # If Pillow fails, try with imageio
    converted_image = convert_dds_to_png_imageio(input_path, output_path)
    if converted_image:
        return converted_image

    # If imageio fails, try with OpenCV
    converted_image = convert_dds_to_png_opencv(input_path, output_path)
    if converted_image:
        return converted_image

    # If OpenCV fails, try with PyGame
    converted_image = convert_dds_to_png_pygame(input_path, output_path)
    if converted_image:
        return converted_image

    # If all else fails, try with DirectXTex
    return convert_dds_to_png_directxtex(input_path, output_path)


def batch_convert_dds_to_png(source_folder, destination_folder):
    global start_time
    total_files = sum(
        len(files) for _, _, files in os.walk(source_folder) if any(file.lower().endswith('.dds') for file in files))
    processed_files = 0

    for dirpath, _, filenames in os.walk(source_folder):
        relative_path = os.path.relpath(dirpath, source_folder)
        target_dir = os.path.join(destination_folder, relative_path)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        dds_files = [f for f in filenames if f.lower().endswith('.dds')]
        for dds_file in dds_files:
            input_path = os.path.join(dirpath, dds_file)
            output_path = os.path.join(target_dir, os.path.splitext(dds_file)[0] + '.png')

            if not os.path.exists(input_path):
                log_message(f"Input file does not exist: {input_path}")
                continue

            converted_image = convert_dds_to_png(input_path, output_path)
            if converted_image:
                show_image_preview(converted_image)
                log_message(f"Converted {input_path} to {output_path}.")
            else:
                log_message(f"Failed to convert {input_path}.")

            processed_files += 1
            update_progress(processed_files, total_files)
            update_eta(processed_files, total_files)


def browse_source_folder():
    folder_selected = filedialog.askdirectory()
    source_folder_var.set(folder_selected)


def browse_destination_folder():
    folder_selected = filedialog.askdirectory()
    destination_folder_var.set(folder_selected)


def start_conversion():
    global start_time
    source_folder = source_folder_var.get()
    destination_folder = destination_folder_var.get()
    if not source_folder or not destination_folder:
        messagebox.showerror("Error", "Please select both source and destination folders.")
        return
    log_message("Starting batch conversion...")
    start_time = time.time()  # Initialize start_time here
    batch_convert_dds_to_png(source_folder, destination_folder)
    end_time = time.time()
    log_message(f"Batch conversion completed in {end_time - start_time:.2f} seconds.")
    messagebox.showinfo("Completed", "Batch conversion completed successfully!")


def log_message(message):
    log_text.config(state=tk.NORMAL)
    log_text.insert(tk.END, message + '\n')
    log_text.config(state=tk.DISABLED)
    log_text.see(tk.END)


def show_image_preview(image):
    if image.mode not in ('RGB', 'RGBA'):
        image = image.convert('RGB')  # Convert image to RGB mode for compatibility
    image.thumbnail((200, 200))
    img = ImageTk.PhotoImage(image)
    image_label.config(image=img)
    image_label.image = img


def update_progress(processed, total):
    progress_var.set((processed / total) * 100)
    progress_bar.update()


def update_eta(processed, total):
    global start_time
    elapsed_time = time.time() - start_time
    if processed == 0:
        eta = 0
    else:
        eta = elapsed_time * (total - processed) / processed
    eta_var.set(f"ETA: {int(eta)} seconds")


# GUI setup
root = tk.Tk()
root.title("DDS to 16-bit PNG Converter")

source_folder_var = tk.StringVar()
destination_folder_var = tk.StringVar()
progress_var = tk.DoubleVar()
eta_var = tk.StringVar()

tk.Label(root, text="Source Folder:").grid(row=0, column=0, padx=10, pady=10)
tk.Entry(root, textvariable=source_folder_var, width=50).grid(row=0, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=browse_source_folder).grid(row=0, column=2, padx=10, pady=10)

tk.Label(root, text="Destination Folder:").grid(row=1, column=0, padx=10, pady=10)
tk.Entry(root, textvariable=destination_folder_var, width=50).grid(row=1, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=browse_destination_folder).grid(row=1, column=2, padx=10, pady=10)

tk.Button(root, text="Start Conversion", command=start_conversion).grid(row=2, column=1, pady=20)

progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100)
progress_bar.grid(row=3, column=1, pady=10)

tk.Label(root, textvariable=eta_var).grid(row=4, column=1)

log_text = tk.Text(root, height=10, width=70, state=tk.DISABLED)
log_text.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

image_label = tk.Label(root)
image_label.grid(row=6, column=0, columnspan=3, padx=10, pady=10)

root.mainloop()

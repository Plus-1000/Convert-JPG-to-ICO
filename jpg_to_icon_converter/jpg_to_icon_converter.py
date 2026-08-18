'''
======Tested by Wang Jian on 2026 Aug 18======
Convert JPG images into ICO icons with ease.
1) Select your preferred icon size.
2) Drag and drop your JPG file into the conversion area.
3) Your new ICO file will be saved in the same folder.

'''
import os
import tkinter as tk
from tkinter import ttk
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import Image, ImageFilter, ImageEnhance

def convert_image(file_path):
    size = int(size_var.get())
    base = os.path.splitext(file_path)[0]
    output_path = base + f"_{size}.ico"

    img = Image.open(file_path).convert("RGBA")

    # High-quality resize
    resized = img.resize((size, size), Image.LANCZOS)

    # Sharpen for crisp edges
    resized = resized.filter(ImageFilter.UnsharpMask(radius=1.5, percent=200, threshold=2))

    # Slight contrast boost
    resized = ImageEnhance.Contrast(resized).enhance(1.08)

    # Save ICO
    resized.save(output_path, format="ICO", sizes=[(size, size)])

    status_label.config(text=f"Saved: {output_path}")

def drop_event(event):
    # Clean path (TkinterDnD gives {C:/path/file.jpg})
    file_path = event.data.strip("{}")
    if file_path.lower().endswith((".jpg", ".jpeg")):
        convert_image(file_path)
    else:
        status_label.config(text="Please drop a JPG file.")

# Create DnD-enabled window
root = TkinterDnD.Tk()
root.title("Drag & Drop JPG → ICO Converter")
root.geometry("400x220")

tk.Label(root, text="Select icon size:").pack(pady=5)

size_var = tk.StringVar(value="64")
size_box = ttk.Combobox(
    root, textvariable=size_var,
    values=["16", "32", "64", "128", "256"],
    state="readonly"
)
size_box.pack(pady=5)

# Drag-and-drop area
drop_label = tk.Label(
    root,
    text="Drag JPG file here",
    relief="solid",
    borderwidth=1,
    width=40,
    height=4
)
drop_label.pack(pady=15)

drop_label.drop_target_register(DND_FILES)
drop_label.dnd_bind("<<Drop>>", drop_event)

status_label = tk.Label(root, text="")
status_label.pack()

root.mainloop()

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import threading

import tkinter as tk
from tkinter import ttk

root = tk.Tk()

# Remove default title bar
root.overrideredirect(True)

# Make window always on top
root.wm_attributes("-topmost", True)

# Create frame for custom title bar
title_bar = ttk.Frame(root, relief='raised', borderwidth=2)

# Add widgets to title bar
close_button = ttk.Button(title_bar, text='X')
title_label = ttk.Label(title_bar, text='My Title')

# Pack widgets into title bar
close_button.pack(side='right')
title_label.pack(side='left')

# Add title bar frame to window
title_bar.pack(fill='x')

# Load and show GIF
# ...existing GIF loading code

# Bind close button
close_button.configure(command=root.destroy)

root.mainloop()


# Create a Tkinter window
root = tk.Tk()

# Function to update the GIF animation
def update_image(image_label, frame_number):
    try:
        photo = gif_frames[frame_number]
    except IndexError:
        frame_number = 0
        photo = gif_frames[frame_number]

    image_label.configure(image=photo)
    frame_number += 1
    root.after(delay, lambda: update_image(image_label, frame_number))

# Open the GIF image
gif_file = Image.open('face1.gif')

# Extract frames
gif_frames = []
try:
    while True:
        frame = ImageTk.PhotoImage(gif_file.copy().convert('RGBA'))
        gif_frames.append(frame)
        gif_file.seek(len(gif_frames))
        delay = gif_file.info['duration']
except EOFError:
    pass

# Create a label with the first frame
image_label = ttk.Label(root, image=gif_frames[0])
image_label.pack()

# Start thread to update the image
threading.Thread(target=update_image, args=(image_label, 0)).start()

# Run the main loop
root.mainloop()

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import threading
import time

# Other imports

# Create root window
root = tk.Tk()
root.overrideredirect(True)

# Dictionary to store GIFs
gifs = {
  'face1.gif': (0, 0),
  'face2.gif': (50, 50),
  'face3.gif': (100, 100)
}



# Function to show GIF
def show_gif(name, x, y):
  # Open GIF
  gif = Image.open(name)

  # Create label
  label = ttk.Label(root)
  label.place(x=x, y=y)

  # Show first frame
  frame = ImageTk.PhotoImage(gif.copy().convert('RGBA'))
  label.config(image=frame)

  # Update thread
  threading.Thread(target=update_gif, args=(label, gif)).start()


# Update gif animation
def update_gif(label, gif):
  frame_num = 0

  while True:
    try:
      frame = ImageTk.PhotoImage(gif.copy().convert('RGBA'))
      label.config(image=frame)
      time.sleep(0.1)
      frame_num += 1
    except EOFError:
      frame_num = 0
      continue


    # Menu bar
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)


# File menu
file_menu = tk.Menu(menu_bar)
menu_bar.add_cascade(label="File", menu=file_menu)

# Start button
def start():
  for name, coords in gifs.items():
    show_gif(name, coords[0], coords[1])

file_menu.add_command(label="Start", command=start)

# Other menu options
file_menu.add_command(label="Stop")
file_menu.add_command(label="Set coordinates")
file_menu.add_command(label="Show coordinates")
file_menu.add_command(label="Set GIF order")
file_menu.add_command(label="Exit", command=root.destroy)

root.mainloop()

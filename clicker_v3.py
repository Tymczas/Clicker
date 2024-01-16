import tkinter as tk
from tkinter import Entry, Button, messagebox, ttk, filedialog
import selenium.webdriver

from selenium import webdriver

from selenium.common.exceptions import NoSuchWindowException, InvalidSessionIdException, WebDriverException
import time
import json

import webbrowser
import requests

# Declare driver as a global variable
driver = []
current_page = 0
rows_per_page = 5


# Function to reset the GUI to its initial state
# Function to reset the GUI to its initial state
def reset_gui():
    global duration_entries  # Declare duration_entries as a global variable


    # Clear existing pages and recreate the default page
    for page in pages:
        page.destroy()
    pages.clear()

    # Explicitly set duration_entries to an empty list
    duration_entries = []



    # Create a new frame for the page
    new_page = ttk.Frame(root)
    new_page.grid(row=2, column=1, columnspan=1, pady=10, padx=1)

    # Add the frame to the list of pages
    pages.append(new_page)

    # Add rows to the page
    add_rows(new_page)

    # Set the current page to the first page
    show_page(0)




# Function to save the current configuration to a selected file
def save_configuration():
    # Ask the user to choose a file path
    file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])

    # Check if the user canceled the file selection
    if not file_path:
        return

    configuration = {
        "url": url_entry.get(),
        "durations": [entry.get() for entry in duration_entries],
        "current_page": current_page,
        # Add more fields as needed
    }

    # Save to the selected file
    with open(file_path, "w") as file:
        json.dump(configuration, file)

# Function to load a configuration from a file
def load_configuration():
    global duration_entries, current_page  # Declare global variables

    reset_gui()  # Reset the GUI before loading a new file

    # Ask the user to choose a file path
    file_path = filedialog.askopenfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])

    # Check if the user canceled the file selection
    if not file_path:
        return

    try:
        with open(file_path, "r") as file:
            configuration = json.load(file)

        # Update the UI based on the loaded configuration
        url_entry.delete(0, tk.END)
        url_entry.insert(0, configuration.get("url", ""))

        # Get the durations from the configuration
        durations = configuration.get("durations", [])

        # Calculate the number of additional pages needed
        num_durations = len(durations)
        num_additional_pages = (num_durations - 1) // rows_per_page

        # Generate additional pages as needed
        for _ in range(num_additional_pages):
            add_page()

        # Insert loaded durations into existing entry widgets
        for i, entry in enumerate(duration_entries):
            if i < num_durations:
                entry.delete(0, tk.END)
                entry.insert(0, str(durations[i]))

        # Set the current page based on the loaded configuration
        current_page = configuration.get("current_page", 0)
        show_page(current_page)

    except Exception as e:
        messagebox.showerror("Error", f"Error loading configuration: {str(e)}")
    show_page(0)



def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def run_script():
    global driver  # Use the global driver variable

    url = url_entry.get()

    try:
        durations = []
        skip_moves = False  # Flag to skip moves if the previous move had a duration of 0

        for i, entry in enumerate(duration_entries):
            duration_text = entry.get()

            # Skip empty entries
            if not duration_text:
                continue

            # Validate numeric input
            if not is_float(duration_text):
                messagebox.showerror("Error", f"Invalid duration in row {i + 1}. Please enter a valid number.")
                return

            # Handle non-negative entries
            duration = float(duration_text)
            if duration < 0:
                messagebox.showerror("Error", f"Duration in row {i + 1} must be a non-negative number.")
                return

            # If the previous move had a duration of 0, skip the subsequent moves
            if skip_moves:
                break

            # Add only non-zero durations to the list
            if duration > 0:
                durations.append((i, duration))
            else:
                skip_moves = True  # Set the flag to skip subsequent moves

        # Check if there is an existing window
        if driver and driver[0].current_url:
            # Switch to the existing window
            driver[0].switch_to.window(driver[0].window_handles[0])
        else:
            # Open a new browser window (Firefox in this case)
            driver.append(webdriver.Firefox())

            # Navigate to the URL
            driver[0].get(url)

        # Get durations from the entry widgets
        webdriver.ActionChains(driver[0]).send_keys(webdriver.Keys.ARROW_UP).perform()

        # Run the script for the specified durations
        for i, duration in durations:
            time.sleep(duration)

            try:
                # Check if the browser window is still open
                if not driver[0].current_url:
                    # Display a message box
                    messagebox.showinfo("Info", "Browser window closed during script execution. Reopening browser.")

                    # Close the current browser window
                    driver[0].quit()

                    # Reopen the browser window
                    driver[0] = webdriver.Firefox()
                    driver[0].get(url)

                # Simulate right arrow key press using Selenium
                webdriver.ActionChains(driver[0]).send_keys(webdriver.Keys.ARROW_RIGHT).perform()

            except (InvalidSessionIdException, NoSuchWindowException, WebDriverException):
                # Handle the case where the browser window is closed during script execution
                # Display a message box
                messagebox.showinfo("Info", "Browser window closed during script execution. Reopening browser.")

                # Close the current browser window
                driver[0].quit()

                # Reopen the browser window
                driver[0] = webdriver.Firefox()
                driver[0].get(url)

    except NoSuchWindowException:
        # Close the current browser window
        driver[0].quit()
        driver[0] = webdriver.Firefox()
        driver[0].get(url)

        # Reopen the browser window
        run_script()


def add_row(page_frame):
    row_number = len(duration_entries) + 1

    label = tk.Label(page_frame, text=f"Move {row_number}:")
    label.grid(padx=1, pady=5, sticky="e")

    entry = Entry(page_frame, width=10)
    entry.grid(padx=1, pady=5)

    entry.delete(0, tk.END)
    entry.insert(0, "1")
    duration_entries.append(entry)

def add_page():
    global current_page
    current_page=len(pages)

    if len(pages) > 0:
        prev_page_button.config(state=tk.NORMAL)
        next_page_button.config(state=tk.NORMAL)

    # Create a new frame for the page
    page_frame = ttk.Frame(root)
    page_frame.grid(row=2, column=1, columnspan=1, pady=10, padx=1)

    # Add the frame to the list of pages
    pages.append(page_frame)

    # Add rows to the page
    add_rows(page_frame)

    # print(current_page)

def add_rows(page_frame):
    for _ in range(rows_per_page):
        add_row(page_frame)

def add_movement():
    add_page()

def on_increment_button_click():
    # Get the currently focused entry
    active_entry = root.focus_get()

    # Check if the focused widget is an Entry and is in duration_entries
    if isinstance(active_entry, Entry) and active_entry in duration_entries:
        current_value = active_entry.get()

        # If the entry has a value, increment it; otherwise, set it to 1
        if current_value:
            current_value = int(current_value)
            active_entry.delete(0, tk.END)
            active_entry.insert(0, str(current_value + 1))
        else:
            active_entry.insert(0, "1")

def on_decrement_button_click():
    # Get the currently focused entry
    active_entry = root.focus_get()

    # Check if the focused widget is an Entry and is in duration_entries
    if isinstance(active_entry, Entry) and active_entry in duration_entries:
        current_value = active_entry.get()

        # If the entry has a value, decrement it; otherwise, set it to 0
        if current_value:
            current_value = int(current_value)
            new_value = max(current_value - 1, 0)  # Allow decrementing to 0
            active_entry.delete(0, tk.END)
            active_entry.insert(0, str(new_value))
        else:
            active_entry.insert(0, "0")



def show_page(page_index):
    global current_page
    if 0 <= page_index < len(pages):
        # Hide all pages
        for page in pages:
            page.grid_forget()

        # Show the selected page
        pages[page_index].grid(row=2, column=1, columnspan=1, pady=10, padx=5)
        current_page = page_index
    # print(current_page)

# Create the main window
root = tk.Tk()
root.title("Selenium Script GUI")

# Create and pack a label for URL
url_label = tk.Label(root, text="Enter URL:")
url_label.grid(row=0, column=0, pady=10)

# Create and pack an entry widget for URL
url_entry = Entry(root, width=30)
url_entry.grid(row=0, column=1, pady=10)

# Set default Lichess URL
default_url = "https://lichess.org/iLxKgl0b"

# Open default URL in new window
webbrowser.open(default_url)

# Lichess API key
lichess_api_key = 'lip_Tn7ko1Q0caCDZyEP9n1T'

# Headers with API key
lichess_headers = {'Authorization': f'Bearer {lichess_api_key}'}

# API endpoint for account info
account_url = 'https://lichess.org/api/account'

# Verify authentication
requests.get(account_url, headers=lichess_headers)

# API endpoint for preferences
preferences_url = 'https://lichess.org/api/account/preferences'

# Preferences settings
lichess_prefs = {
  'pieceSet': 'cburnett',
  'boardTheme': 'blue',
  'background': 'blue'
}

# Update preferences
requests.put(preferences_url, headers=lichess_headers, json=lichess_prefs)



# Create and pack entry widgets for durations
duration_entries = []

# List to store page frames
pages = []

# Buttons for navigating between pages
prev_page_button = tk.Button(root, text="Previous", command=lambda: show_page(current_page - 1), state=tk.DISABLED)
prev_page_button.grid(row=4, column=0, pady=10, padx=1)

next_page_button = tk.Button(root, text="Next", command=lambda: show_page(current_page + 1), state=tk.DISABLED)
next_page_button.grid(row=4, column=2, pady=10, padx=1)


add_movement_button = tk.Button(root, text="Add Moves", command=add_movement)
add_movement_button.grid(row=4, column=1, pady=10, padx=1)



# Create and pack buttons for incrementing and decrementing move entry
decrement_button = tk.Button(root, text="-", command=on_decrement_button_click, height=20, width=6)
decrement_button.grid(row=2, column=1, pady=10, padx=1,sticky='w')


increment_button = tk.Button(root, text="+", command=on_increment_button_click, height=20, width=6)
increment_button.grid(row=2, column=1, pady=10, padx=1,sticky='e')


save_button = tk.Button(root, text="Save", command=save_configuration)
save_button.grid(row=5, column=1, columnspan=2, pady=10, padx=50,sticky='w')

# Create a button for loading configuration
load_button = tk.Button(root, text="Load", command=load_configuration)
load_button.grid(row=5, column=1, columnspan=1, pady=10, padx=50,sticky='e')

# Create and pack a button
button = tk.Button(root, text="Run Script", command=run_script, fg='green')
button.grid(row=6, column=1, columnspan=1, pady=3,padx=5)

# Create and pack an exit button
exit_button = tk.Button(root, text="Exit", command=root.destroy)
exit_button.grid(row=8, column=1, columnspan=1, pady=1,padx=5)



# Example usage
add_page()

# Run the GUI
root.mainloop()

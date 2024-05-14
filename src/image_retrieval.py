import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import json
import os
from tkcalendar import DateEntry

def search_json_and_display_images():
    search_term = entry_search.get()
    search_category = variable.get()
    images_folder = 'saved_images/'  # Change this to your folder path

    try:
        found_uuids = []
        with open('index_data.json') as f:
            data = json.load(f)
            for uuid, values in data.items():
                if search_term == values.get(search_category):
                    found_uuids.append(uuid)

        if found_uuids:
            global current_image_index
            current_image_index = 0
            global image_paths
            image_paths = [os.path.join(images_folder, uuid + '.jpg') for uuid in found_uuids]
            display_image()
        else:
            messagebox.showinfo("Search Result", "No UUIDs found for the given search term.")
    except FileNotFoundError:
        messagebox.showerror("File Not Found", "The JSON file does not exist.")

def display_image():
    global current_image_index
    if image_paths:
        if current_image_index >= len(image_paths):
            current_image_index = 0
        elif current_image_index < 0:
            current_image_index = len(image_paths) - 1

        image_path = image_paths[current_image_index]
        if os.path.exists(image_path):
            image = Image.open(image_path)
            image.thumbnail((600, 600))  # Resize the image to fit in the window
            photo = ImageTk.PhotoImage(image)

            image_label.configure(image=photo)
            image_label.image = photo  # Keep a reference to the image to prevent garbage collection
        else:
            messagebox.showwarning("Image Not Found", f"Image not found: {image_path}")

def next_image():
    global current_image_index
    current_image_index += 1
    display_image()

def previous_image():
    global current_image_index
    current_image_index -= 1
    display_image()

def change_search_input(selected_category):
    if selected_category == "date":
        entry_search.grid_forget()
        date_entry.grid(row=2, column=1, sticky="ew")
    else:
        date_entry.grid_forget()
        entry_search.grid(row=2, column=1, sticky="ew")

# Create Tkinter window
root = tk.Tk()
root.title("JSON Search and Image Display")

# Set a fixed size for the window
root.geometry("800x600")

# Create entry widget for search term input
label_search = tk.Label(root, text="Select Search Category:")
label_search.grid(row=1, column=0)
categories = ["date", "row", "stalks"]
variable = tk.StringVar(root)
variable.set(categories[0])
dropdown_menu = tk.OptionMenu(root, variable, *categories, command=change_search_input)
dropdown_menu.grid(row=1, column=1, sticky="ew")

entry_search = tk.Entry(root)
entry_search.grid(row=2, column=1, sticky="ew")

# Create DateEntry widget for date input
date_entry = DateEntry(root, width=12, background='darkblue', foreground='white', borderwidth=2)
date_entry.grid(row=2, column=1, sticky="ew")
date_entry.grid_forget()  # Initially hide the date entry

# Call change_search_input with the default category
change_search_input(categories[0])

# Create search button
search_button = tk.Button(root, text="Search JSON and Display Images", command=search_json_and_display_images)
search_button.grid(row=3, column=1, pady=5)

# Create label for displaying images
image_label = tk.Label(root)
image_label.grid(row=4, column=0, columnspan=2)

# Create buttons for navigating through images
button_previous = tk.Button(root, text="Previous", command=previous_image)
button_previous.grid(row=5, column=0, padx=5, pady=5)

button_next = tk.Button(root, text="Next", command=next_image)
button_next.grid(row=5, column=1, padx=5, pady=5)

current_image_index = 0  # Index to keep track of current image being displayed
image_paths = []

root.mainloop()

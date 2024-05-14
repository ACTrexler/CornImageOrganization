import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import json
import os
from tkcalendar import DateEntry

class ImageRetrievingWindow:
    def __init__(self, master):

        # Create Tkinter window
        self.master = master
        self.master.title("Image Retrieving")
        self.master.geometry("700x700")

        # Create entry widget for search term input
        self.label_search = tk.Label(self.master, text="Select Search Category:")
        self.label_search.grid(row=1, column=0)
        self.categories = ["date", "row", "stalks"]
        self.variable = tk.StringVar(self.master)
        self.variable.set(self.categories[0])
        self.dropdown_menu = tk.OptionMenu(self.master, self.variable, *self.categories, command=self.change_search_input)
        self.dropdown_menu.grid(row=1, column=1, sticky="ew")

        self.entry_search = tk.Entry(self.master)
        self.entry_search.grid(row=2, column=1, sticky="ew")

        # Create DateEntry widget for date input
        self.date_entry = DateEntry(self.master, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.date_entry.grid(row=2, column=1, sticky="ew")
        self.date_entry.grid_forget()  # Initially hide the date entry

        # Call change_search_input with the default category
        self.change_search_input(self.categories[0])

        # Create search button
        self.search_button = tk.Button(self.master, text="Search JSON and Display Images", command=self.search_json_and_display_images)
        self.search_button.grid(row=3, column=1, pady=5)

        # Create label for displaying images
        self.image_label = tk.Label(self.master)
        self.image_label.grid(row=4, column=0, columnspan=2)

        # Create buttons for navigating through images
        self.button_previous = tk.Button(self.master, text="Previous", command=self.previous_image)
        self.button_previous.grid(row=5, column=0, padx=5, pady=5)

        self.button_next = tk.Button(self.master, text="Next", command=self.next_image)
        self.button_next.grid(row=5, column=1, padx=5, pady=5)

        self.current_image_index = 0  # Index to keep track of current image being displayed
        self.image_paths = []

    def search_json_and_display_images(self):
        search_term = self.entry_search.get()
        search_category = self.variable.get()
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
                self.display_image()
            else:
                messagebox.showinfo("Search Result", "No UUIDs found for the given search term.")
        except FileNotFoundError:
            messagebox.showerror("File Not Found", "The JSON file does not exist.")

    def display_image(self):
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

                self.image_label.configure(image=photo)
                self.image_label.image = photo  # Keep a reference to the image to prevent garbage collection
            else:
                messagebox.showwarning("Image Not Found", f"Image not found: {image_path}")

    def next_image(self):
        global current_image_index
        current_image_index += 1
        self.display_image()

    def previous_image(self):
        global current_image_index
        current_image_index -= 1
        self.display_image()

    def change_search_input(self, selected_category):
        if selected_category == "date":
            self.entry_search.grid_forget()
            self.date_entry.grid(row=2, column=1, sticky="ew")
        else:
            self.date_entry.grid_forget()
            self.entry_search.grid(row=2, column=1, sticky="ew")

def main():
    root = tk.Tk()
    app = ImageRetrievingWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()

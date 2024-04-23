import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from tkcalendar import DateEntry
from datetime import date, datetime
import os
from shutil import copyfile
import uuid
import os
import json

INDEX_DATA_FILE = "index_data.json"

class ImageDocumentingWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Image Documenting")
        self.master.geometry("900x500")

        self.image_list = []
        self.original_paths = []
        self.descriptions_row = []
        self.descriptions_stalks = []
        self.current_index = 0

        self.canvas = tk.Canvas(self.master, width=700, height=400)
        self.canvas.pack(pady=10)

        self.date_selector = DateEntry(self.master, width=12, date_pattern='mm-dd-yyyy')
        self.date_selector.pack(side=tk.LEFT, padx=10)
        self.date_selector.set_date(datetime.now())

        self.label_row = tk.Label(self.master, text="Row:")
        self.label_row.pack(side=tk.LEFT, padx=10)
        self.entry_description_row = tk.Entry(self.master, width=25)
        self.entry_description_row.pack(side=tk.LEFT)

        self.label_stalks = tk.Label(self.master, text="Stalks:")
        self.label_stalks.pack(side=tk.LEFT, padx=10)
        self.entry_description_stalks = tk.Entry(self.master, width=25)
        self.entry_description_stalks.pack(side=tk.LEFT)

        self.btn_prev = tk.Button(self.master, text="Previous", command=self.show_previous)
        self.btn_prev.pack(side=tk.LEFT, padx=10)

        self.btn_next = tk.Button(self.master, text="Next", command=self.show_next)
        self.btn_next.pack(side=tk.LEFT, padx=10)

        self.btn_browse = tk.Button(self.master, text="Browse Images", command=self.browse_images)
        self.btn_browse.pack(side=tk.LEFT, pady=10)

        self.btn_save = tk.Button(self.master, text="Save Images", command=self.save_images)
        self.btn_save.pack(side=tk.LEFT, pady=10)

    def browse_images(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("JPEG files", "*.jpg *.jpeg")])
        for file_path in file_paths:
            self.original_paths.append(file_path)
            image = Image.open(file_path)
            width, height = image.size
            if width > 700 or height > 400:
                if width / height > 700 / 400:
                    new_width = 700
                    new_height = int(height * (700 / width))
                else:
                    new_height = 400
                    new_width = int(width * (400 / height))
                image = image.resize((new_width, new_height), Image.LANCZOS)
            self.image_list.append(ImageTk.PhotoImage(image))
            self.descriptions_row.append("")
            self.descriptions_stalks.append("")
        if self.image_list:
            self.show_image()

    def show_image(self):
        self.canvas.delete("all")
        self.canvas.create_image(350, 200, image=self.image_list[self.current_index])
        self.entry_description_row.delete(0, tk.END)
        if self.descriptions_row[self.current_index] == "" and self.current_index > 0:
            self.entry_description_row.insert(tk.END, self.descriptions_row[self.current_index - 1])
        else:
            self.entry_description_row.insert(tk.END, self.descriptions_row[self.current_index])
        self.entry_description_stalks.delete(0, tk.END)
        if self.descriptions_stalks[self.current_index] == "" and self.current_index > 0:
            self.entry_description_stalks.insert(tk.END, self.descriptions_stalks[self.current_index - 1])
        else:
            self.entry_description_stalks.insert(tk.END, self.descriptions_stalks[self.current_index])

    def show_previous(self):
        if self.current_index > 0:
            self.descriptions_row[self.current_index] = self.entry_description_row.get()
            self.descriptions_stalks[self.current_index] = self.entry_description_stalks.get()
            self.current_index -= 1
            self.show_image()

    def show_next(self):
        if self.current_index < len(self.image_list) - 1:
            self.descriptions_row[self.current_index] = self.entry_description_row.get()
            self.descriptions_stalks[self.current_index] = self.entry_description_stalks.get()
            self.current_index += 1
            self.show_image()

    def save_images(self):
        if not self.image_list:
            return
        directory = filedialog.askdirectory()
        if directory:
            unique_ids = []
            for i, original_path in enumerate(self.original_paths):
                #description_row = self.descriptions_row[i]
                #description_stalks = self.descriptions_stalks[i]
                unique_id = uuid.uuid4().hex[:6]
                unique_ids.append(unique_id)
                file_name = f"{unique_id}.jpg"
                file_path = os.path.join(directory, file_name)
                copyfile(original_path, file_path)
            index_data = self.generate_index_data(unique_ids)
            save_index_to_file(index_data, INDEX_DATA_FILE)
    
    def generate_index_data(self, uuids):
        index_data = {}
        for i in range(len(uuids)):
            uuid = uuids[i]
            data = {"date": self.date_selector.get_date(), "row": self.descriptions_row[i], "stalks": self.descriptions_stalks[i]}
            index_data[uuid] = data
        return index_data


def save_index_to_file(index_data, filename):
    file_path = os.path.join(os.getcwd(), filename)

    if os.path.exists(file_path):
        # Load existing data and update it with new data
        existing_data = load_index_from_file(filename)
        existing_data.update(index_data)
        index_data = existing_data

    with open(filename, 'w') as file:
        json.dump(index_data, file, default=json_serial)

def load_index_from_file(filename):
    if not os.path.exists(filename):
        return {}  # Return an empty dictionary if file doesn't exist

    with open(filename, 'r') as file:
        index_data = json.load(file)
    return index_data

def json_serial(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()

def main():
    root = tk.Tk()
    app = ImageDocumentingWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()

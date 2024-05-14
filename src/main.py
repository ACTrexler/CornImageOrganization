import tkinter as tk
from tkinter import messagebox
import image_retrieval
import image_documenting

class MainWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Main Window")
        self.master.geometry("400x200")
        
        self.label = tk.Label(self.master, text="Choose a program to open:")
        self.label.pack(pady=20)
        
        self.button1 = tk.Button(self.master, text="Open Image Documenting", command=self.open_documenting)
        self.button1.pack(pady=10)
        
        self.button2 = tk.Button(self.master, text="Open Image Retrieval", command=self.open_retrieval)
        self.button2.pack(pady=10)
        
    def open_documenting(self):
        self.new_window = tk.Toplevel(self.master)
        self.app = image_documenting.ImageDocumentingWindow(self.new_window)
        
    def open_retrieval(self):
        self.new_window = tk.Toplevel(self.master)
        self.app = image_retrieval.ImageRetrievingWindow(self.new_window)

if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()

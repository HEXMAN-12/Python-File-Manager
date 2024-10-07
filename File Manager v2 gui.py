import os
import shutil
import send2trash
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

class FileManager(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Python File Manager")
        self.geometry("600x400")

        self.current_path = os.getcwd()

        self.create_widgets()

    def create_widgets(self):
        # Navigation Buttons
        self.path_label = tk.Label(self, text=self.current_path)
        self.path_label.pack()

        self.listbox = tk.Listbox(self, selectmode=tk.SINGLE)
        self.listbox.pack(fill=tk.BOTH, expand=1)
        self.listbox.bind('<Double-1>', self.on_item_selected)

        self.populate_listbox()

        self.buttons_frame = tk.Frame(self)
        self.buttons_frame.pack(fill=tk.X)

        self.open_button = tk.Button(self.buttons_frame, text="Open", command=self.open_item)
        self.open_button.pack(side=tk.LEFT)

        self.rename_button = tk.Button(self.buttons_frame, text="Rename", command=self.rename_item)
        self.rename_button.pack(side=tk.LEFT)

        self.move_button = tk.Button(self.buttons_frame, text="Move", command=self.move_item)
        self.move_button.pack(side=tk.LEFT)

        self.copy_button = tk.Button(self.buttons_frame, text="Copy", command=self.copy_item)
        self.copy_button.pack(side=tk.LEFT)

        self.delete_button = tk.Button(self.buttons_frame, text="Delete", command=self.delete_item)
        self.delete_button.pack(side=tk.LEFT)

        self.search_button = tk.Button(self.buttons_frame, text="Search", command=self.search_item)
        self.search_button.pack(side=tk.LEFT)

        self.back_button = tk.Button(self.buttons_frame, text="Back", command=self.go_back)
        self.back_button.pack(side=tk.LEFT)

    def populate_listbox(self):
        self.listbox.delete(0, tk.END)
        self.path_label.config(text=self.current_path)
        try:
            for item in os.listdir(self.current_path):
                self.listbox.insert(tk.END, item)
        except PermissionError:
            messagebox.showerror("Error", "Permission Denied")

    def on_item_selected(self, event):
        selected_item = self.listbox.get(self.listbox.curselection())
        selected_path = os.path.join(self.current_path, selected_item)
        if os.path.isdir(selected_path):
            self.current_path = selected_path
            self.populate_listbox()
        else:
            os.startfile(selected_path)

    def open_item(self):
        selected_item = self.listbox.get(self.listbox.curselection())
        selected_path = os.path.join(self.current_path, selected_item)
        if os.path.isdir(selected_path):
            self.current_path = selected_path
            self.populate_listbox()
        else:
            os.startfile(selected_path)

    def rename_item(self):
        selected_item = self.listbox.get(self.listbox.curselection())
        selected_path = os.path.join(self.current_path, selected_item)
        new_name = simpledialog.askstring("Rename", "Enter new name:", initialvalue=selected_item)
        if new_name:
            new_path = os.path.join(self.current_path, new_name)
            shutil.move(selected_path, new_path)
            self.populate_listbox()

    def move_item(self):
        selected_item = self.listbox.get(self.listbox.curselection())
        selected_path = os.path.join(self.current_path, selected_item)
        new_directory = filedialog.askdirectory()
        if new_directory:
            shutil.move(selected_path, new_directory)
            self.populate_listbox()

    def copy_item(self):
        selected_item = self.listbox.get(self.listbox.curselection())
        selected_path = os.path.join(self.current_path, selected_item)
        new_directory = filedialog.askdirectory()
        if new_directory:
            if os.path.isdir(selected_path):
                shutil.copytree(selected_path, os.path.join(new_directory, os.path.basename(selected_path)))
            else:
                shutil.copy(selected_path, new_directory)
            self.populate_listbox()

    def delete_item(self):
        selected_item = self.listbox.get(self.listbox.curselection())
        selected_path = os.path.join(self.current_path, selected_item)
        if messagebox.askyesno("Delete", f"Are you sure you want to delete {selected_item}?"):
            if os.path.isdir(selected_path):
                shutil.rmtree(selected_path)
            else:
                os.unlink(selected_path)
            self.populate_listbox()

    def search_item(self):
        query = simpledialog.askstring("Search", "Enter the name of the file or folder to search for:")
        if query:
            self.listbox.delete(0, tk.END)
            self.search_recursive(self.current_path, query)

    def search_recursive(self, directory, query):
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            if query.lower() in item.lower():
                self.listbox.insert(tk.END, item_path)
            if os.path.isdir(item_path):
                self.search_recursive(item_path, query)

    def go_back(self):
        self.current_path = os.path.dirname(self.current_path)
        self.populate_listbox()

if __name__ == "__main__":
    app = FileManager()
    app.mainloop()

import os
import shutil
import send2trash
import customtkinter as ctk
from tkinter import filedialog, messagebox, simpledialog, Listbox, END

class FileManager(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Python File Manager")
        self.geometry("1060x600")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.current_path = os.getcwd()
        self.common_locations = {
            "Documents": os.path.expanduser("~/Documents"),
            "Videos": os.path.expanduser("~/Videos"),
            "Pictures": os.path.expanduser("~/Pictures"),
            "Downloads": os.path.expanduser("~/Downloads")
        }

        self.create_widgets()

    def create_widgets(self):
        # Top Frame for Path Display and Navigation Buttons
        top_frame = ctk.CTkFrame(self, corner_radius=10)
        top_frame.pack(fill=ctk.X, padx=10, pady=10)

        self.path_label = ctk.CTkLabel(top_frame, text=self.current_path, anchor='w')
        self.path_label.pack(fill=ctk.X, padx=10, pady=10)

        # Main Frame
        main_frame = ctk.CTkFrame(self, corner_radius=10)
        main_frame.pack(fill=ctk.BOTH, expand=1, padx=10, pady=10)

        # Left Frame for Common Locations
        left_frame = ctk.CTkFrame(main_frame, corner_radius=10)
        left_frame.pack(side=ctk.LEFT, fill=ctk.Y, padx=10, pady=10)

        self.locations_listbox = Listbox(left_frame, bg="#2b2b2b", fg="white", selectbackground="#3d85c6", highlightthickness=0)
        self.locations_listbox.pack(fill=ctk.BOTH, expand=1, padx=10, pady=10)
        self.locations_listbox.bind('<Double-1>', self.on_location_selected)

        self.populate_locations()

        # Right Frame for File List
        right_frame = ctk.CTkFrame(main_frame, corner_radius=10)
        right_frame.pack(side=ctk.RIGHT, fill=ctk.BOTH, expand=1, padx=10, pady=10)

        self.listbox = Listbox(right_frame, bg="#2b2b2b", fg="white", selectbackground="#3d85c6", highlightthickness=0)
        self.listbox.pack(fill=ctk.BOTH, expand=1, padx=10, pady=10)
        self.listbox.bind('<Double-1>', self.on_item_selected)

        self.populate_listbox()

        # Bottom Frame for Action Buttons
        bottom_frame = ctk.CTkFrame(self, corner_radius=10)
        bottom_frame.pack(fill=ctk.X, padx=10, pady=10)

        self.open_button = ctk.CTkButton(bottom_frame, text="Open", command=self.open_item)
        self.open_button.pack(side=ctk.LEFT, padx=5, pady=5)

        self.rename_button = ctk.CTkButton(bottom_frame, text="Rename", command=self.rename_item)
        self.rename_button.pack(side=ctk.LEFT, padx=5, pady=5)

        self.move_button = ctk.CTkButton(bottom_frame, text="Move", command=self.move_item)
        self.move_button.pack(side=ctk.LEFT, padx=5, pady=5)

        self.copy_button = ctk.CTkButton(bottom_frame, text="Copy", command=self.copy_item)
        self.copy_button.pack(side=ctk.LEFT, padx=5, pady=5)

        self.delete_button = ctk.CTkButton(bottom_frame, text="Delete", command=self.delete_item)
        self.delete_button.pack(side=ctk.LEFT, padx=5, pady=5)

        self.search_button = ctk.CTkButton(bottom_frame, text="Search", command=self.search_item)
        self.search_button.pack(side=ctk.LEFT, padx=5, pady=5)

        self.back_button = ctk.CTkButton(bottom_frame, text="Back", command=self.go_back)
        self.back_button.pack(side=ctk.LEFT, padx=5, pady=5)

    def populate_listbox(self):
        self.listbox.delete(0, END)
        self.path_label.configure(text=self.current_path)
        try:
            for item in os.listdir(self.current_path):
                self.listbox.insert(END, item)
        except PermissionError:
            messagebox.showerror("Error", "Permission Denied")

    def populate_locations(self):
        for name in self.common_locations.keys():
            self.locations_listbox.insert(END, name)

    def on_location_selected(self, event):
        selected_item = self.locations_listbox.get(self.locations_listbox.curselection())
        selected_path = self.common_locations[selected_item]
        if os.path.isdir(selected_path):
            self.current_path = selected_path
            self.populate_listbox()

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
            self.listbox.delete(0, END)
            self.search_recursive(self.current_path, query)

    def search_recursive(self, directory, query):
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            if query.lower() in item.lower():
                self.listbox.insert(END, item_path)
            if os.path.isdir(item_path):
                self.search_recursive(item_path, query)

    def go_back(self):
        self.current_path = os.path.dirname(self.current_path)
        self.populate_listbox()

if __name__ == "__main__":
    app = FileManager()
    app.mainloop()

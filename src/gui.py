import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import atlas_parser as atlas
import os

window_title = "DD1 Skin Mod Fixer"
window_size = "450x460"

class ModFixerApp(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title(window_title)
        self.geometry(window_size)
        self.setup_widgets()
    
    def setup_widgets(self):
        self.mod_path_label = tk.Label(self, text = "Mod Folder: Please provide the mod folder path here.")
        self.mod_path_label.pack()
        
        self.mod_path_entry = tk.Entry(self)
        self.mod_path_entry.pack()

        self.process_mod_button = tk.Button(self, text="Process all the mods in the mod folder", command = self.on_process_click)
        self.process_mod_button.pack()

        self.restore_button = tk.Button(self, text="Restore the mod", command = self.on_restore_click)
        self.restore_button.pack()

        self.browse_button = tk.Button(self, text="Browse", command=self.on_browse_click)
        self.browse_button.pack()

    def on_process_click(self):
        parent_folder = self.mod_path_entry.get()
        mod_folders = [os.path.join(parent_folder, d) for d in os.listdir(parent_folder) 
                   if os.path.isdir(os.path.join(parent_folder, d))]
        atlas.process_multiple_mods(mod_folders)
        messagebox.showinfo("Success","All mods processed!")
    
    def on_restore_click(self):
        parent_folder = self.mod_path_entry.get()
        mod_folders = [os.path.join(parent_folder, d) for d in os.listdir(parent_folder) 
                   if os.path.isdir(os.path.join(parent_folder, d))]
        for mod_folder in mod_folders:
            atlas.restore_backup(mod_folder)
        messagebox.showinfo("Success","All mods restored!")

    def on_browse_click(self):
        folder = filedialog.askdirectory()
        if folder:
            self.mod_path_entry.delete(0, "end")
            self.mod_path_entry.insert(0, folder)

if __name__ == "__main__":
    app = ModFixerApp()
    app.mainloop()
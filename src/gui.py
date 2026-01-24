import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import atlas_parser as atlas
import os
import ctypes
import sys

window_title = "DD1 Skin Mod Fixer"
window_size = "545x150"

class ModFixerApp(tk.Tk):

    def resource_path(self, relative_path):
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.dirname(__file__), relative_path)

    def __init__(self):
        super().__init__()
        self.title(window_title)
        self.geometry(window_size)
        self.iconbitmap(self.resource_path("assets/preview_icon.ico"))
        self.resizable(False, False)
        self.setup_widgets()
    
    def setup_widgets(self):
        self.mod_path_label = tk.Label(self, text = "Mod Folder:")
        self.mod_path_label.pack(padx=(38, 10), pady=(10, 0), anchor="w")

        self.path_frame = tk.Frame(self)
        self.path_frame.pack(padx=10, pady=0)        
        
        self.mod_path_entry = tk.Entry(self.path_frame, width=40)
        self.mod_path_entry.pack(side="left", padx=(0, 10), pady=5)

        self.button_frame = tk.Frame(self)
        self.button_frame.pack(padx=10, pady=3)

        self.restore_button = tk.Button(self.button_frame, text="Restore the mod", width=22, command = self.on_restore_click)
        self.restore_button.pack(side="left", padx=(10, 25), pady=5)

        self.process_mod_button = tk.Button(self.button_frame, text="Process Mod Folder", width=22, command = self.on_process_click)
        self.process_mod_button.pack(side="left", padx=(24, 10), pady=5)

        self.browse_button = tk.Button(self.path_frame, text="Browse", width=8, command=self.on_browse_click)
        self.browse_button.pack(side="left", padx=5, pady=5)

    def on_process_click(self):
        parent_folder = self.mod_path_entry.get()
        
        if not parent_folder:
            messagebox.showerror("Error", "Please select a mod folder first.")
            return
        
        if not os.path.exists(parent_folder):
            messagebox.showerror("Error", f"Folder does not exist:\n{parent_folder}")
            return

        mod_folders = [os.path.join(parent_folder, d) for d in os.listdir(parent_folder) 
                   if os.path.isdir(os.path.join(parent_folder, d))]
        
        if not mod_folders:
            messagebox.showwarning("Warning", "No subfolders found in the selected folder.")
            return

        results = atlas.process_multiple_mods(mod_folders)

        success_count = len(results["success"])
        skipped_count = len(results["skipped"])
        error_count = len(results["error"])
    
        message = f"Processing complete!\n\n"
        message += f"Success: {success_count}\n"
        message += f"Skipped: {skipped_count}\n"
        message += f"Errors: {error_count}"

        if results["error"]:
            message += "\n\nFailed mods:\n"
            for err in results["error"]:
                message += f"• {err['mod_name']}: {err['reason']}\n"

        if results["skipped"]:
            message += "\n\nSkipped mods:\n"
            for skip in results["skipped"]:
                message += f"• {skip['mod_name']}: {skip['reason']}\n"
        
        messagebox.showinfo("Results", message)
    
    def on_restore_click(self):
        parent_folder = self.mod_path_entry.get()

        if not parent_folder:
            messagebox.showerror("Error", "Please select a mod folder first.")
            return
        
        if not os.path.exists(parent_folder):
            messagebox.showerror("Error", f"Folder does not exist:\n{parent_folder}")
            return

        mod_folders = [os.path.join(parent_folder, d) for d in os.listdir(parent_folder) 
                   if os.path.isdir(os.path.join(parent_folder, d))]
        
        if not mod_folders:
            messagebox.showwarning("Warning", "No subfolders found.")
            return
    
        restored = 0
        skipped = 0
        errors = 0

        for mod_folder in mod_folders:
            try:
                if atlas.restore_backup(mod_folder):
                    restored += 1
                else:
                    skipped += 1
            except Exception as e:
                print(f"Could not restore {os.path.basename(mod_folder)}: {e}")    

        message = f"Restored: {restored}\nNo backup found: {skipped}"
        if errors > 0:
            message += f"\nErrors: {errors}"
        if restored > 0:
            messagebox.showinfo("Done", message)
        elif errors > 0:
            messagebox.showerror("Error", message)
        else:
            messagebox.showwarning("Warning", message)

    def on_browse_click(self):
        folder = filedialog.askdirectory()
        if folder:
            self.mod_path_entry.delete(0, "end")
            self.mod_path_entry.insert(0, folder)

ctypes.windll.shcore.SetProcessDpiAwareness(1)

if __name__ == "__main__":
    app = ModFixerApp()
    app.mainloop()
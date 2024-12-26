from tkinter import ttk
import tkinter as tk
import pickle

class ClipboardManager:
    def __init__(self, root, history_count):
        self.root = root
        self.clipboard_history = []
        self.current_clipboard = self.get_clipboard()
        self.history_count = history_count
        self.create_ui()

    def create_ui(self):
        self.root.title("Clipboard Manager")
        self.root.configure(bg="#F0F0F0")
        self.root.geometry("400x500")

        frame = ttk.Frame(self.root, padding=6)
        frame.pack(fill='both', expand=True)

        search_frame = ttk.Frame(frame)
        search_frame.pack(fill='x')

        search_label = ttk.Label(search_frame, text="Search:")
        search_label.pack(side='left')

        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.pack(side='left', fill='x', expand=True)
        self.search_entry.bind("<KeyRelease>", self.search_clipboard)

        self.listbox = tk.Listbox(frame, font=("Arial", 10), selectbackground="#D3D3D3")
        self.listbox.pack(side='left', fill='both', expand=True)

        scrollbar = ttk.Scrollbar(frame, command=self.listbox.yview)
        scrollbar.pack(side='right', fill='y')

        self.listbox.config(yscrollcommand=scrollbar.set)
        self.listbox.bind("<Up>", self.select_previous)
        self.listbox.bind("<Down>", self.select_next)
        self.listbox.bind("<ButtonRelease>", self.on_select) # Copy text on mouse click
        self.listbox.bind("<Return>", self.on_select) # Copy text on Enter key press

    def get_clipboard(self):
        try:
            return self.root.clipboard_get()
        except tk.TclError:
            return ''

    def search_clipboard(self, event):
        search_text = self.search_entry.get().lower()
        self.listbox.delete(0, tk.END)
        for item in self.clipboard_history:
            if search_text in item.lower():
                self.listbox.insert(tk.END, item)

    def update_clipboard(self):
        current_clipboard = self.get_clipboard()
        if current_clipboard != self.current_clipboard and current_clipboard.strip() != '':
            if current_clipboard in self.clipboard_history:
                # alredy exist in history, so remove it so that it can be added on top
                elements = self.listbox.get(0, tk.END)
                self.listbox.delete(elements.index(current_clipboard))
                self.clipboard_history.remove(current_clipboard)

            # add current clipboard to top of history
            self.current_clipboard = current_clipboard
            self.clipboard_history.append(current_clipboard)
            self.listbox.insert(0, current_clipboard)

            if len(self.clipboard_history) > self.history_count:
                self.clipboard_history = self.clipboard_history[:self.history_count]
                self.listbox.delete(self.history_count)

    def on_select(self, event):
        self.copy_selected_text()

    def select_previous(self, event):
        current_selection = self.listbox.curselection()
        if current_selection:
            previous_index = current_selection[0] - 1
            if previous_index >= 0:
                self.listbox.selection_clear(0, tk.END)
                self.listbox.selection_set(previous_index)
                self.listbox.see(previous_index)
                self.copy_selected_text()

    def select_next(self, event):
        current_selection = self.listbox.curselection()
        if current_selection:
            next_index = current_selection [0] + 1
            if next_index < self.listbox.size():
                self.listbox.selection_clear(0, tk.END)
                self.listbox.selection_set (next_index)
                self.listbox.see(next_index)
                self.copy_selected_text()

    def copy_selected_text(self):
        selection = self.listbox.curselection()
        if selection:
            selected_text = self.listbox.get(selection[0])
            self.root.clipboard_clear()
            self.root.clipboard_append(selected_text)
            self.current_clipboard = selected_text

    def save_history_to_file(self, filepath):
        with open(filepath, 'wb') as file:
            pickle.dump(self.clipboard_history, file)

    def load_history_from_file(self, filepath):
        try:
            with open(filepath, 'rb') as file:
                self.clipboard_history = pickle.load(file)
                for item in self.clipboard_history:
                    self.listbox.insert(0, item)
        except FileNotFoundError:
            pass

    def run (self):
        self.update_clipboard()
        self.root.after(500, self.run)

def main():
    root = tk.Tk()
    clipboard_manager = ClipboardManager(root, history_count=1000)
    clipboard_manager.run()
    def save_and_close():
        clipboard_manager.save_history_to_file("clipboard_history.pkl")
        root.destroy()
    root.protocol ("WM_DELETE_WINDOW", save_and_close)
    root.mainloop()

if __name__ == "__main__":
    main()
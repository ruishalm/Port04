import tkinter as tk
from tkinter import ttk

class Postit(tk.Frame):
    def __init__(self, parent, title, content=""):
        super().__init__(parent)
        self.title = title
        self.content = content
        self.create_widgets()

    def create_widgets(self):
        self.title_label = ttk.Label(self, text=self.title, font=('Helvetica', 16, 'bold'))
        self.title_label.pack()

        self.content_text = tk.Text(self, wrap='word', height=1)
        self.content_text.insert('1.0', self.content)
        self.content_text.pack(expand=True, fill='both')

    def adjust_size(self):
        lines = self.content_text.get("1.0", "end-1c").split("\n")
        max_length = max(len(line) for line in lines)
        self.content_text.config(width=max_length, height=len(lines))

    def set_content(self, content):
        self.content = content
        self.content_text.delete("1.0", "end")
        self.content_text.insert("1.0", content)
        self.adjust_size()

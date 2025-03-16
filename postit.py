import tkinter as tk
from tkinter import ttk
from utils import get_formated_date

class Postit:
    def __init__(self, master, date, selfcare=False, model=None): # agora o construtor precisa receber o model
        self.date = date
        self.content = ""
        self.model = model # e ele fica salvo aqui
        self.create_widgets(master, selfcare)

    def create_widgets(self, master, selfcare):
        self.frame = ttk.Frame(master, padding="5", relief=tk.RIDGE, borderwidth=2)
        if not selfcare:
            date_label = ttk.Label(self.frame, text=get_formated_date(self.date))
        else:
            date_label = ttk.Label(self.frame, text=f"Selfcare - {get_formated_date(self.date)}")
        date_label.pack()

        self.text_widget = tk.Text(self.frame, height=5, width=20)
        self.text_widget.pack(expand=True, fill='both')

        self.save_button = ttk.Button(self.frame, text="Salvar", command=self.save)
        self.save_button.pack(pady=(5, 0))

    def get_content(self):
        return self.text_widget.get("1.0", tk.END).strip()

    def set_content(self, content):
        self.text_widget.insert(tk.END, content)

    def save(self):
        content = self.text_widget.get("1.0", tk.END).strip()
        if self.model:
            self.model.save_postit(self.date, content) # agora pode chamar o save, pois tem acesso ao model.

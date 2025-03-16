import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style
from datetime import datetime, timedelta
from postit import Postit

class Interface:
    def __init__(self, root):
        self.root = root
        self.style = Style(theme='darkly')
        self.root.geometry("800x600")
        self.current_date = datetime.now()
        self.postits = {}  # Dicionário para armazenar o conteúdo dos post-its
        self.next_week_items = ["aquele agradinho que mereco"]  # Lista para armazenar itens para a próxima semana
        self.previous_week_items = ["aquele agradinho que mereco"]  # Lista para armazenar itens da semana anterior
        self.create_widgets()
        self.create_postits()

    def create_widgets(self):
        # Cabeçalho
        self.header_frame = ttk.Frame(self.root, padding="10")
        self.header_frame.grid(row=0, column=0, columnspan=4, sticky="ew")

        self.prev_button = ttk.Button(self.header_frame, text="<- Semana Anterior", command=self.prev_week, cursor="hand2")
        self.prev_button.grid(row=0, column=0, sticky="w")

        self.date_label = ttk.Label(self.header_frame, text=self.get_header_text(), font=("Helvetica", 20, "bold"))
        self.date_label.grid(row=0, column=1, columnspan=2, sticky="ew")

        self.next_button = ttk.Button(self.header_frame, text="Próxima Semana ->", command=self.next_week, cursor="hand2")
        self.next_button.grid(row=0, column=3, sticky="e")

        # Ajusta as colunas para expandirem proporcionalmente
        self.header_frame.columnconfigure(2, weight=1)

        # Seção "Itens da Semana Anterior"
        self.previous_week_frame = ttk.Frame(self.root, padding="10", relief=tk.RIDGE, borderwidth=2)
        self.previous_week_frame.grid(row=1, column=0, sticky="ew")

        self.previous_week_label = ttk.Label(self.previous_week_frame, text="Da Semana Passada", font=("Helvetica", 12, "bold"))
        self.previous_week_label.pack()

        # Corpo principal
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=2, column=0, sticky="nsew")

        # Ajusta o frame principal para expandir
        self.root.rowconfigure(2, weight=1)
        self.root.columnconfigure(0, weight=1)

        # Seção "Para a Próxima Semana"
        self.next_week_frame = ttk.Frame(self.root, padding="10")
        self.next_week_frame.grid(row=3, column=0, sticky="ew")

        self.next_week_label = ttk.Label(self.next_week_frame, text="Para a Próxima Semana", font=("Helvetica", 16, "bold"))
        self.next_week_label.grid(row=0, column=0, columnspan=3)

        self.next_week_text = tk.Text(self.next_week_frame, height=5, width=40)
        self.next_week_text.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        self.arrow_label = ttk.Label(self.next_week_frame, text="->", font=("Helvetica", 16, "bold"))
        self.arrow_label.grid(row=1, column=1, padx=5, pady=5)

        self.next_week_preview = tk.Text(self.next_week_frame, height=5, width=40, state='disabled')
        self.next_week_preview.grid(row=1, column=2, padx=5, pady=5, sticky="nsew")

        self.next_week_save_button = ttk.Button(self.next_week_frame, text="Adicionar", command=self.save_next_week_item)
        self.next_week_save_button.grid(row=2, column=0, columnspan=3)

        # Ajusta as colunas e linhas para expandirem proporcionalmente
        self.next_week_frame.columnconfigure(0, weight=1)
        self.next_week_frame.columnconfigure(2, weight=1)
        self.next_week_frame.rowconfigure(1, weight=1)

        self.update_next_week_preview()
        self.load_previous_week_items()

    def get_header_text(self):
        start_of_week = self.current_date - timedelta(days=(self.current_date.weekday() + 1) % 7)
        end_of_week = start_of_week + timedelta(days=6)
        current_day = self.current_date.strftime("%d, %a")
        start_date = start_of_week.strftime("%d/%m")
        end_date = end_of_week.strftime("%d/%m")
        return f"dia {current_day} - semana {start_date} ate {end_date}"

    def create_postits(self):
        # Limpa os post-its antigos
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Cria novos post-its
        for i in range(8):  # Supondo que há 7 dias na semana + 1 para selfcare
            day_frame = ttk.Frame(self.main_frame, padding="5", relief=tk.RIDGE, borderwidth=2)
            day_frame.grid(row=i // 4, column=i % 4, padx=5, pady=5, sticky="nsew")

            if i < 7:
                date_label = ttk.Label(day_frame, text=(self.current_date - timedelta(days=(self.current_date.weekday() + 1) % 7) + timedelta(days=i)).strftime("%A, %d %B"))
            else:
                date_label = ttk.Label(day_frame, text=f"Selfcare - {self.current_date.strftime('%d %B %Y')}")

            date_label.pack()

            text_widget = tk.Text(day_frame, height=5, width=20)
            text_widget.pack(expand=True, fill='both')

            save_button = ttk.Button(day_frame, text="Salvar", command=lambda i=i: self.save_postit(i, text_widget))
            save_button.pack(pady=(5, 0))  # Adiciona um pouco de espaço acima do botão

            if i in self.postits:
                text_widget.insert(tk.END, self.postits[i])

            # Ajusta dinamicamente o tamanho da caixa de texto e da fonte
            text_widget.bind("<KeyRelease>", lambda event, widget=text_widget: self.adjust_text_widget_size(widget))

        # Ajusta as colunas e linhas para expandirem proporcionalmente
        for i in range(4):
            self.main_frame.columnconfigure(i, weight=1)
        for i in range(2):  # Ajusta para 2 linhas
            self.main_frame.rowconfigure(i, weight=1)

    def adjust_text_widget_size(self, text_widget):
        lines = text_widget.get("1.0", "end-1c").split("\n")
        max_length = max(len(line) for line in lines)
        text_widget.config(width=max_length, height=len(lines))

        # Ajusta dinamicamente o tamanho da fonte
        font_size = max(8, 20 - len(lines))  # Exemplo de cálculo de tamanho da fonte
        text_widget.config(font=("Helvetica", font_size))

    def save_postit(self, day_index, text_widget):
        self.postits[day_index] = text_widget.get("1.0", tk.END).strip()

    def save_next_week_item(self):
        item = self.next_week_text.get("1.0", tk.END).strip()
        if item:
            self.next_week_items.append(item)
            self.next_week_text.delete("1.0", tk.END)
            self.update_next_week_preview()

    def update_next_week_preview(self):
        self.next_week_preview.config(state='normal')
        self.next_week_preview.delete("1.0", tk.END)
        for item in self.next_week_items:
            self.next_week_preview.insert(tk.END, f"- {item}\n")
        self.next_week_preview.config(state='disabled')

    def prev_week(self):
        self.current_date -= timedelta(days=7)
        self.date_label.config(text=self.get_header_text())
        self.create_postits()
        self.load_previous_week_items()

    def next_week(self):
        self.current_date += timedelta(days=7)
        self.date_label.config(text=self.get_header_text())
        self.create_postits()
        self.transfer_next_week_items()
        self.load_previous_week_items()

    def transfer_next_week_items(self):
        # Transferir itens da "Próxima Semana" para "Itens da Semana Anterior"
        self.previous_week_items = self.next_week_items.copy()
        self.next_week_items.clear()
        self.update_next_week_preview()

    def load_previous_week_items(self):
        # Limpar a seção de itens da semana anterior
        for widget in self.previous_week_frame.winfo_children():
            if widget != self.previous_week_label:
                widget.destroy()

        # Adicionar borda e título
        if self.previous_week_items:
            for item in self.previous_week_items:
                checkbox = ttk.Checkbutton(self.previous_week_frame, text=item)
                checkbox.pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = Interface(root)
    root.mainloop()

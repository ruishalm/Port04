import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style
from utils import get_formated_date
from widgets import (
    create_next_week_frame,
    create_previous_week_frame,
    create_theme_selector,
    create_postits,
    update_next_week_preview,
)
import tkinter.font as tkFont


class Interface:
    def __init__(self, root, model):
        self.root = root
        self.model = model
        self.style = Style(theme=self.get_current_theme())
        self.root.geometry("800x600")
        self.create_watermark()
        self.create_widgets()
        # variaveis auxiliares
        self.edit_mode = False
        self.current_index = None

    def create_widgets(self):
        header_font = tkFont.Font(family="Helvetica", size=20, weight="bold")

        self.header_frame = ttk.Frame(self.root, padding="10")
        self.header_frame.grid(row=0, column=0, columnspan=4, sticky="ew")

        self.prev_button = ttk.Button(
            self.header_frame, text="<- Semana Anterior", command=self.prev_week, cursor="hand2"
        )
        self.prev_button.grid(row=0, column=0, sticky="w")

        self.current_day_label = ttk.Label(
            self.header_frame, text=self.get_current_day_text(), font=header_font
        )
        self.current_day_label.grid(row=0, column=1, sticky="w")

        self.date_label = ttk.Label(self.header_frame, text=self.get_current_week_text(), font=header_font)
        self.date_label.grid(row=0, column=2, sticky="e")

        self.next_button = ttk.Button(
            self.header_frame, text="Próxima Semana ->", command=self.next_week, cursor="hand2"
        )
        self.next_button.grid(row=0, column=3, sticky="e")

        self.header_frame.columnconfigure(2, weight=1)

        # Chamando a funcao que criar o Frame, que foi movido para outro arquivo
        self.previous_week_frame = create_previous_week_frame(self.root)
        self.previous_week_frame.grid(row=1, column=0, sticky="ew")

        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=2, column=0, sticky="nsew")

        self.root.rowconfigure(2, weight=1)
        self.root.columnconfigure(0, weight=1)

        # Chamando a funcao que criar o Frame, que foi movido para outro arquivo
        self.next_week_frame = create_next_week_frame(self.root, self)
        self.next_week_frame.grid(row=3, column=0, sticky="ew")

        # Chamando a funcao que criar o Theme Selector, que foi movido para outro arquivo
        create_theme_selector(self.root, self)
        # Ajustar a linha do seletor de temas
        self.root.rowconfigure(4, weight=0)

        # Chamando a funcao que criar os postits, que foi movido para outro arquivo
        create_postits(self.main_frame, self.model)
        # Mudança aqui: Atualizando a tela após inserir o item no Model
        self.update_next_week_preview()

        self.update_header_labels()
        self.load_previous_week_items()
        self.adjust_header_font_size(header_font)

    def get_current_day_text(self):
        current_day = get_formated_date(self.model.current_date, day_name=True)
        return f"{current_day}"

    def get_current_week_text(self):
        dates = self.model.get_week_dates()
        start_date = get_formated_date(dates[0])
        end_date = get_formated_date(dates[-1])
        return f"Semana: {start_date} até {end_date}"

    def prev_week(self):
        self.model.change_week(-7)
        create_postits(self.main_frame, self.model)
        self.load_previous_week_items()
        self.update_header_labels()

    def next_week(self):
        self.model.change_week(7)
        create_postits(self.main_frame, self.model)
        self.transfer_next_week_items()
        self.load_previous_week_items()
        self.update_header_labels()

    def update_header_labels(self):
        self.current_day_label.config(text=self.get_current_day_text())
        self.date_label.config(text=self.get_current_week_text())

    def transfer_next_week_items(self):
        self.model.transfer_next_week_items()
        self.update_next_week_preview()

    def load_previous_week_items(self):
        from widgets import load_previous_week_items

        load_previous_week_items(self.previous_week_frame, self.model)

    def adjust_header_font_size(self, header_font):
        header_width = self.header_frame.winfo_width()

        if header_width > 700:
            new_font_size = 20
        elif header_width > 500:
            new_font_size = 16
        else:
            new_font_size = 12
        header_font.configure(size=new_font_size)

    def create_watermark(self):
        from datetime import datetime

        current_year = datetime.now().year
        self.watermark_label = tk.Label(
            self.root, text=str(current_year), font=("Helvetica", 48, "bold"), fg="gray", bd=0, compound="center"
        )
        root_bg = self.root.cget("background")
        self.watermark_label.config(bg=root_bg)
        transparent_image = tk.PhotoImage(width=1, height=1)
        self.watermark_label.config(image=transparent_image, compound="center")
        self.watermark_label.place(relx=0.5, rely=0.5, relwidth=1, relheight=1, anchor="center")
        self.watermark_label.lower()

    def change_theme(self, new_theme):
        self.style.theme_use(new_theme)
        self.set_current_theme(new_theme)
        self.watermark_label.config(bg=self.root.cget("background"))
        self.create_watermark()

    def get_current_theme(self):
        from utils import load_data

        themes = load_data("themes.json")
        if not themes:
            return "flatly"
        return themes.get("current_theme")

    def set_current_theme(self, theme):
        from utils import save_data

        themes = load_data("themes.json")
        if not themes:
            themes = {}
        themes["current_theme"] = theme
        save_data("themes.json", themes)

    def update_next_week_preview(self):
        update_next_week_preview(self)

    # Mudança aqui: Funcao de editar item
    def edit_item(self, event):
        try:
            self.edit_mode = True
            selected_index = self.next_week_preview.curselection()[0]
            selected_item = self.next_week_preview.get(selected_index)
            self.current_index = selected_item
            self.next_week_text.delete("1.0", tk.END)
            self.next_week_text.insert(tk.END, selected_item)
            self.next_week_save_button.config(text="Atualizar")
        except IndexError:
            pass

    # Mudança aqui: Funcoes de Drag and Drop
    def on_drag_start(self, event):
        self.current_index = self.next_week_preview.nearest(event.y)

    def on_drag_motion(self, event):
        new_index = self.next_week_preview.nearest(event.y)

        if new_index != self.current_index:
            item = self.next_week_preview.get(self.current_index)
            self.next_week_preview.delete(self.current_index)
            self.next_week_preview.insert(new_index, item)
            self.current_index = new_index
            self.model.reorder_next_week_item(self.current_index)
    def remove_selected_item(self):
        try:
            selected_index = self.next_week_preview.curselection()[0]
            selected_item = self.next_week_preview.get(selected_index)
            self.model.remove_next_week_item(selected_item)
            self.update_next_week_preview()
        except IndexError:
            pass
    def save_next_week_item(self):
        item = self.next_week_text.get("1.0", tk.END).strip()
        if item:
            if self.edit_mode:
                # Mudança aqui: Editar o item, e não apendar ele.
                self.model.edit_next_week_item(self.current_index, item)
                self.next_week_save_button.config(text="Adicionar")
                self.edit_mode = False
            else:
                self.model.add_next_week_item(item)
            self.next_week_text.delete("1.0", tk.END)
            self.update_next_week_preview()


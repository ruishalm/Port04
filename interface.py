import tkinter as tk
from tkinter import ttk, StringVar
from ttkbootstrap import Style
from datetime import timedelta, datetime
from utils import get_formated_date, clear_frame, load_data, save_data
from postit import Postit
import tkinter.font as tkFont


class Interface:
    def __init__(self, root, model):
        self.root = root
        self.model = model
        self.style = Style(theme=self.get_current_theme())
        self.root.geometry("800x600")
        self.create_watermark()
        self.create_widgets()

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

        self.previous_week_frame = ttk.Frame(self.root, padding="10", relief=tk.RIDGE, borderwidth=2)
        self.previous_week_frame.grid(row=1, column=0, sticky="ew")

        self.previous_week_label = ttk.Label(
            self.previous_week_frame, text="Da Semana Passada", font=("Helvetica", 12, "bold")
        )
        self.previous_week_label.pack()

        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=2, column=0, sticky="nsew")

        self.root.rowconfigure(2, weight=1)
        self.root.columnconfigure(0, weight=1)

        # Mudança aqui: Ajustando a largura das Text Areas.
        self.next_week_frame = ttk.Frame(self.root, padding="10")
        self.next_week_frame.grid(row=3, column=0, sticky="ew")

        self.next_week_label = ttk.Label(
            self.next_week_frame, text="Para a Próxima Semana", font=("Helvetica", 16, "bold")
        )
        self.next_week_label.grid(row=0, column=0, columnspan=3)

        self.next_week_text = tk.Text(self.next_week_frame, height=5, width=30)
        self.next_week_text.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        self.arrow_label = ttk.Label(self.next_week_frame, text="->", font=("Helvetica", 16, "bold"))
        self.arrow_label.grid(row=1, column=1, padx=5, pady=5)

        self.next_week_preview = tk.Listbox(self.next_week_frame, height=5, width=30, bg="#f0f0f0")
        self.next_week_preview.grid(row=1, column=2, padx=5, pady=5, sticky="nsew")

        self.next_week_save_button = ttk.Button(
            self.next_week_frame, text="Adicionar", command=self.save_next_week_item
        )
        self.next_week_save_button.grid(row=2, column=0)
        # Add the remove button
        self.remove_button = ttk.Button(self.next_week_frame, text="Remover", command=self.remove_selected_item)
        self.remove_button.grid(row=2, column=2)

        self.next_week_frame.columnconfigure(0, weight=1)
        self.next_week_frame.columnconfigure(2, weight=1)
        self.next_week_frame.rowconfigure(1, weight=1)
        # Theme Selection
        self.create_theme_selector()

        # Ajustar a linha do seletor de temas
        self.root.rowconfigure(4, weight=0)

        self.update_next_week_preview()
        self.load_previous_week_items()
        self.create_postits()
        self.update_header_labels()
        self.adjust_header_font_size(header_font)

    def create_postits(self):
        clear_frame(self.main_frame)

        dates = self.model.get_week_dates()
        for i, date in enumerate(dates):
            postit = Postit(self.main_frame, date, model=self.model)
            postit.frame.grid(row=i // 4, column=i % 4, padx=5, pady=5, sticky="nsew")
            content = self.model.get_postit(date)
            if content:
                postit.set_content(content)

        date = self.model.get_selfcare_date()
        postit = Postit(
            self.main_frame, date, selfcare=True, model=self.model
        )
        postit.frame.grid(row=1, column=3, padx=5, pady=5, sticky="nsew")
        content = self.model.get_postit(date)
        if content:
            postit.set_content(content)

        for i in range(4):
            self.main_frame.columnconfigure(i, weight=1)
        for i in range(2):
            self.main_frame.rowconfigure(i, weight=1)
        self.update_header_labels()

    def get_current_day_text(self):
        current_day = get_formated_date(self.model.current_date, day_name=True)
        return f"{current_day}"

    def get_current_week_text(self):
        dates = self.model.get_week_dates()
        start_date = get_formated_date(dates[0])
        end_date = get_formated_date(dates[-1])
        return f"Semana: {start_date} até {end_date}"

    def save_next_week_item(self):
        item = self.next_week_text.get("1.0", tk.END).strip()
        if item:
            self.model.add_next_week_item(item)
            self.next_week_text.delete("1.0", tk.END)
            self.update_next_week_preview()

    def update_next_week_preview(self):
        self.next_week_preview.delete(0, tk.END)
        # Mudança aqui: Inserindo os itens da model, na tela.
        for item in self.model.get_next_week_items():
            self.next_week_preview.insert(tk.END, item)

    def prev_week(self):
        self.model.change_week(-7)
        self.create_postits()
        self.load_previous_week_items()
        self.update_header_labels()

    def next_week(self):
        self.model.change_week(7)
        self.create_postits()
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
        clear_frame(self.previous_week_frame)

        if self.model.get_previous_week_items():
            for item in self.model.get_previous_week_items():
                checkbox = ttk.Checkbutton(self.previous_week_frame, text=item)
                checkbox.pack()

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

    def create_theme_selector(self):
        self.theme_names = self.style.theme_names()
        self.theme_var = StringVar(value=self.get_current_theme())

        self.theme_frame = ttk.Frame(self.root)
        # Mudança aqui: Usando grid
        self.theme_frame.grid(row=4, column=0, sticky="se")

        # Add the label here
        theme_label = ttk.Label(self.theme_frame, text="Tema:")
        theme_label.pack(side="left", padx=(0, 5))

        self.theme_menu = ttk.OptionMenu(
            self.theme_frame,
            self.theme_var,
            self.get_current_theme(),
            *self.theme_names,
            command=self.change_theme,
        )
        self.theme_menu.pack(side="left")

    def get_current_theme(self):
        themes = load_data("themes.json")
        if not themes:
            return "flatly"
        return themes.get("current_theme")

    def set_current_theme(self, theme):
        themes = load_data("themes.json")
        if not themes:
            themes = {}
        themes["current_theme"] = theme
        save_data("themes.json", themes)

    def remove_selected_item(self):
        try:
            selected_index = self.next_week_preview.curselection()[0]
            selected_item = self.next_week_preview.get(selected_index)
            self.model.remove_next_week_item(selected_item)
            self.update_next_week_preview()
        except IndexError:
            pass

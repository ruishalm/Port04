import tkinter as tk
from tkinter import ttk
from postit import Postit
from utils import clear_frame
import tkinter.font as tkFont
from PIL import Image, ImageTk, ImageDraw, ImageFont


def create_next_week_frame(master, interface):
    """Cria o frame 'Para a Próxima Semana'."""
    next_week_frame = ttk.Frame(master, padding="10")

    next_week_label = ttk.Label(
        next_week_frame, text="Para a Próxima Semana", font=("Helvetica", 16, "bold")
    )
    next_week_label.grid(row=0, column=0, columnspan=3, sticky="ew")

    next_week_text = tk.Text(next_week_frame, height=5)
    next_week_text.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
    interface.next_week_text = next_week_text

    arrow_label = ttk.Label(next_week_frame, text="->", font=("Helvetica", 16, "bold"))
    arrow_label.grid(row=1, column=1, padx=5, pady=5)

    next_week_preview = tk.Listbox(next_week_frame, bg="#f0f0f0", height=5)
    next_week_preview.grid(row=1, column=2, padx=5, pady=5, sticky="nsew")
    interface.next_week_preview = next_week_preview

    next_week_preview.bind("<Double-Button-1>", interface.edit_item)
    next_week_preview.bind("<Button-1>", interface.on_drag_start)
    next_week_preview.bind("<B1-Motion>", interface.on_drag_motion)

    next_week_save_button = ttk.Button(
        next_week_frame, text="Adicionar", command=interface.save_next_week_item
    )
    next_week_save_button.grid(row=2, column=0, sticky="ew")
    interface.next_week_save_button = next_week_save_button

    remove_button = ttk.Button(next_week_frame, text="Remover", command=interface.remove_selected_item)
    remove_button.grid(row=2, column=2, sticky="ew")

    return next_week_frame


def create_previous_week_frame(master):
    """Cria o frame 'Da Semana Passada'."""
    previous_week_frame = ttk.Frame(master, padding="10", relief=tk.RIDGE, borderwidth=2)
    font_label = tkFont.Font(family="Helvetica", size=12, weight="bold")

    previous_week_info = ttk.Label(previous_week_frame, text="Itens pendentes da semana anterior:", font=font_label, foreground="#333333")
    previous_week_info.pack(pady=(10, 5), fill="x")

    previous_week_label = ttk.Frame(previous_week_frame)
    previous_week_label.pack()

    return previous_week_frame


def create_theme_selector(master, interface):
    """Cria o seletor de temas."""
    theme_names = interface.style.theme_names()
    theme_var = tk.StringVar(value=interface.get_current_theme())

    theme_frame = ttk.Frame(master)
    theme_frame.grid(row=4, column=0, sticky="se")

    theme_label = ttk.Label(theme_frame, text="Tema:")
    theme_label.pack(side="left", padx=(0, 5))

    theme_menu = ttk.OptionMenu(
        theme_frame,
        theme_var,
        interface.get_current_theme(),
        *theme_names,
        command=interface.change_theme,
    )
    theme_menu.pack(side="left")


def create_postits(master, model):
    """Cria os Post-its da semana."""
    clear_frame(master)

    dates = model.get_week_dates()
    for i, date in enumerate(dates):
        postit = Postit(master, date, model=model)
        postit.frame.grid(row=i // 4, column=i % 4, padx=5, pady=5, sticky="nsew")
        content = model.get_postit(date)
        if content:
            postit.set_content(content)

    date = model.get_selfcare_date()
    postit = Postit(master, date, selfcare=True, model=model)
    postit.frame.grid(row=1, column=3, padx=5, pady=5, sticky="nsew")
    content = model.get_postit(date)
    if content:
        postit.set_content(content)

    for i in range(4):
        master.columnconfigure(i, weight=1)
    for i in range(2):
        master.rowconfigure(i, weight=1)


def update_next_week_preview(interface):
    """Atualiza a Listbox 'Para a Próxima Semana'."""
    interface.next_week_preview.delete(0, tk.END)
    for item in interface.model.get_next_week_items():
        interface.next_week_preview.insert(tk.END, item)


def load_previous_week_items(previous_week_frame, model):
    """Carrega os itens da semana anterior."""
    previous_week_label = previous_week_frame.winfo_children()[1]
    clear_frame(previous_week_label)

    if model.get_previous_week_items():
        for index, (key, item) in enumerate(model.get_previous_week_items().items()):
            checkbox = ttk.Checkbutton(previous_week_label, text=item)
            checkbox.pack()

def create_rotated_label(master, text, color, font_name, size):
    """Cria um Label com texto rotacionado em 45 graus usando PIL."""
    font = ImageFont.truetype(font_name + ".ttf", size)
    image = Image.new("RGBA", (500, 500), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)
    draw.text((250, 250), text, fill=color, font=font, anchor="mm")
    rotated_image = image.rotate(45, expand=True, resample=Image.BICUBIC)
    photo = ImageTk.PhotoImage(rotated_image)
    label = tk.Label(master, image=photo, bd=0)
    label.image = photo
    label.config(bg=master.cget("background"))
    return label

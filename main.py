import tkinter as tk
from interface import Interface
from model import PlannerModel

if __name__ == "__main__":
    root = tk.Tk()
    model = PlannerModel()  # Cria a instância do Model
    app = Interface(root, model)  # Passa o Model para a Interface
    root.mainloop()

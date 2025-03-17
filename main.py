import tkinter as tk
from interface import Interface
from model import PlannerModel

if __name__ == "__main__":
    root = tk.Tk()
    model = PlannerModel()  # Criar a instância do Model
    app = Interface(root, model)  # Passar o Model para a Interface
    model.interface = app # Mudança aqui: passar o app para o Model
    root.mainloop()

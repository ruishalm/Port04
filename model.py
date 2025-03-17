from datetime import datetime, timedelta
from utils import save_data, load_data

class PlannerModel:
    def __init__(self):
        self.current_date = datetime.now()
        self.postits = load_data("postits.json")
        self.next_week_items = load_data("next_week.json")
        # Correção aqui: Atributo estava incompleto
        self.previous_week_items = load_data("previous_week.json")

        if not isinstance(self.next_week_items, list):
            self.next_week_items = []
        if not isinstance(self.postits, dict):
            self.postits = {}

        if not isinstance(self.previous_week_items, dict):
            self.previous_week_items = {}
        # Mudança aqui: Criando um novo atributo para salvar a interface.
        self.interface = None
        # Correção aqui: Vamos garantir que "Aquele agradinho merecido" esteja na lista, caso a semana mude.
        self.ensure_agradinho_is_present()
    
    def ensure_agradinho_is_present(self):
        selfcare_date_str = self.get_selfcare_date().strftime("%d/%m/%Y")
        if selfcare_date_str not in self.postits:
            self.postits[selfcare_date_str] = "Aquele agradinho merecido"
            save_data("postits.json", self.postits)

    # Mudança aqui: Funcao para pegar a data do selfcare
    def get_selfcare_date(self):
        next_week_start = self.get_week_dates()[0] + timedelta(weeks=1)
        selfcare_date = next_week_start + timedelta(days=0) #  primeira segunda-feira da semana seguinte.
        return selfcare_date
    
    def get_week_dates(self):
        start_of_week = self.current_date - timedelta(days=self.current_date.weekday())
        return [start_of_week + timedelta(days=i) for i in range(7)]

    # Resto do código (sem alterações no momento)
    # ...
    
    def save_postit(self, date, content):
        date_str = date.strftime("%d/%m/%Y")
        self.postits[date_str] = content
        save_data("postits.json", self.postits)
    
    # rest of code...
    #...
    def get_postit(self, date):
        date_str = date.strftime("%d/%m/%Y")
        return self.postits.get(date_str, "")
    
    def change_week(self, days):
        self.current_date += timedelta(days=days)
        self.ensure_agradinho_is_present()

    def add_next_week_item(self, item):
        self.next_week_items.append(item)
        save_data("next_week.json", self.next_week_items)

    def get_next_week_items(self):
        return self.next_week_items

    def remove_next_week_item(self, item):
        if item in self.next_week_items:
            self.next_week_items.remove(item)
            save_data("next_week.json", self.next_week_items)
    
    def edit_next_week_item(self, old_item, new_item):
        index = self.next_week_items.index(old_item)
        self.next_week_items[index] = new_item
        save_data("next_week.json", self.next_week_items)
    
    def reorder_next_week_item(self, item):
        index = self.next_week_items.index(item)
        self.next_week_items.pop(index)
        self.next_week_items.insert(index, item)
        save_data("next_week.json", self.next_week_items)

    def transfer_next_week_items(self):
        next_week_dates = self.get_week_dates()
        
        # Se nao existe nada no postit daquele dia, adicionar o item que veio do proxima semana
        if not self.previous_week_items:
            for item in self.next_week_items:
                self.previous_week_items[len(self.previous_week_items)] = item
        else:
             for item in self.next_week_items:
                self.previous_week_items[len(self.previous_week_items)] = item

        self.next_week_items = []
        save_data("next_week.json", self.next_week_items)
        save_data("previous_week.json", self.previous_week_items)

    def get_previous_week_items(self):
        return self.previous_week_items

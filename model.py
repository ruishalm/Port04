from datetime import datetime, timedelta
from utils import save_data, load_data

class PlannerModel:
    def __init__(self):
        self.current_date = datetime.now()
        self.postits = load_data("postits.json")
        # Mudança aqui: Inicializando como lista vazia
        self.next_week_items = load_data("next_week.json")
        self.previous_week_items = load_data("previous_week.json")
        
        if not isinstance(self.next_week_items, list):
            self.next_week_items = []
        # check if self.postits is a dict, if not, make it a dict
        if not isinstance(self.postits, dict):
            self.postits = {}

    def get_postit(self, date):
        return self.postits.get(date.strftime("%Y-%m-%d"))

    def save_postit(self, date, content):
        self.postits[date.strftime("%Y-%m-%d")] = content
        save_data("postits.json", self.postits)

    def add_next_week_item(self, item):
        self.next_week_items.append(item)
        save_data("next_week.json", self.next_week_items)

    def remove_next_week_item(self, item):
        if item in self.next_week_items:
            self.next_week_items.remove(item)
            save_data("next_week.json", self.next_week_items)

    def get_next_week_items(self):
        return self.next_week_items

    def transfer_next_week_items(self):
        self.previous_week_items = self.next_week_items.copy()
        self.next_week_items.clear()
        save_data("next_week.json", self.next_week_items)
        save_data("previous_week.json", self.previous_week_items)

    def get_previous_week_items(self):
        return self.previous_week_items
    
    def get_week_dates(self):
        start_of_week = self.current_date - timedelta(days=(self.current_date.weekday() + 1) % 7)
        return [start_of_week + timedelta(days=i) for i in range(7)]

    def get_selfcare_date(self):
        return self.current_date
    
    def change_week(self, days):
        self.current_date += timedelta(days=days)


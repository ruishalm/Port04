from datetime import timedelta

# Funções utilitárias (exemplo)
def format_date(date):
    return date.strftime("%d/%m/%Y")

def get_start_of_week(date):
    return date - timedelta(days=(date.weekday() + 1) % 7)

def get_end_of_week(date):
    return get_start_of_week(date) + timedelta(days=6)

def get_formated_date(date, day_name=False, month_name=False): # Mudança aqui: add mes_name
    if day_name:
        return date.strftime("%a, %d/%m")
    elif month_name: # Mudança aqui: criar a verificação se tem que retornar o mes
        return date.strftime("%d de %B") # Mudança aqui: Retornando o dia e o mes por extenso.
    else:
        return date.strftime("%d/%m")

def save_data(file_name, data):
    import json
    with open(file_name, "w") as f:
        json.dump(data, f)

def load_data(file_name):
    import json
    try:
        with open(file_name, "r") as f:
            data = json.load(f)
            # Check if loaded data is a dict, if so, return it.
            if isinstance(data, dict):
                return data
            else:
                return []  # if is not a dict, return a empty list.
    except FileNotFoundError:
        return {}  # if the file does not exist, return an empty dict.

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

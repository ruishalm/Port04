import json
from postit import Postit

def save_postits(postits, filename="postits.json"):
    with open(filename, "w") as file:
        json.dump([postit.__dict__ for postit in postits], file)

def load_postits(filename="postits.json"):
    try:
        with open(filename, "r") as file:
            postits_data = json.load(file)
            return [Postit(**data) for data in postits_data]
    except FileNotFoundError:
        return []

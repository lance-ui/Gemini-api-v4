import json
import os

def read_history(uid, chat_type='default'):
    filename = f"{uid}{'_c' if chat_type == 'character' else ''}.json"
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []
    except Exception as e:
        print(f"Error reading history: {e}")
        return []

def save_history(uid, history, chat_type='default'):
    filename = f"{uid}{'_c' if chat_type == 'character' else ''}.json"
    with open(filename, "w") as f:
        json.dump(history, f, indent=4)
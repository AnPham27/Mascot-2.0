import json
import os

CONFIG_FILE = "config.json"

def load_config():
    """Reads config.json, or returns defaults if missing"""

    if not os.path.exists(CONFIG_FILE):
        return {"divisions": {}, "playoff_dates": [], "holidays": [], "standings":{}}

    with open(CONFIG_FILE, "r") as f:
        return json.load(f)
    


def save_config(config):
    """Writes updated config to file"""

    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)






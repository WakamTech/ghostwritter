import json
import os
import csv

CONFIG_DIR = 'ghost_app/config'  # Directory to store config files

def ensure_config_dir_exists():
    """Ensures the configuration directory exists, creates it if not."""
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)

def save_config_to_json(config_data, filename):
    """Saves configuration data to a JSON file."""
    ensure_config_dir_exists()
    filepath = os.path.join(CONFIG_DIR, filename)
    with open(filepath, 'w') as f:
        json.dump(config_data, f, indent=4) # indent=4 for pretty formatting

def load_config_from_json(filename):
    """Loads configuration data from a JSON file. Returns an empty dictionary if file not found or error occurs."""
    filepath = os.path.join(CONFIG_DIR, filename)
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {} # Return empty dict if file doesn't exist
    except json.JSONDecodeError:
        print(f"Error decoding JSON from {filename}. Returning empty config.")
        return {} # Return empty dict if JSON is invalid


# Specific save/load functions for each config type
def save_general_config(config_data):
    save_config_to_json(config_data, 'general_config.json')

def load_general_config():
    return load_config_from_json('general_config.json')

def save_openai_config(config_data):
    save_config_to_json(config_data, 'openai_config.json')

def load_openai_config():
    return load_config_from_json('openai_config.json')

def save_wordpress_config(config_data):
    save_config_to_json(config_data, 'wordpress_config.json')

def load_wordpress_config():
    return load_config_from_json('wordpress_config.json')

SITES_KEYWORDS_FILE = 'sites_keywords.csv' # Define filename for sites_keywords

def load_sites_keywords():
    """Loads sites and keywords from sites_keywords.csv. Returns a list of dictionaries."""
    filepath = SITES_KEYWORDS_FILE  # Use the defined filename
    sites_keywords_data = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f) # Use DictReader for easier access by header
            for row in reader:
                sites_keywords_data.append(row) # DictReader returnsOrderedDict, converting to regular dict is often fine
    except FileNotFoundError:
        print(f"Error: {filepath} not found. Returning empty sites/keywords list.")
    return sites_keywords_data


def save_sites_keywords(sites_keywords_list):
    """Saves the list of sites and keywords (dictionaries) to sites_keywords.csv."""
    filepath = SITES_KEYWORDS_FILE
    fieldnames = ['url', 'keyword'] # Define fieldnames explicitly here
    try:
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames) # Initialize DictWriter with fieldnames
            writer.writeheader()
            writer.writerows(sites_keywords_list)
        print(f"Sites and keywords successfully saved to {filepath}")
    except Exception as e:
        print(f"Error saving sites and keywords to {filepath}: {e}")
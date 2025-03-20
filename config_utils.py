import csv

def load_config_from_csv(filepath):
    """Loads configurations from a CSV file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        row = next(reader)
        return dict(zip(header, row))

def load_prompt_from_txt(filepath):
    """Loads a prompt from a TXT file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

# No changes to load_prompt_from_txt needed
import csv

def load_config_from_csv(filepath):
    """Charge les configurations depuis un fichier CSV."""
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        row = next(reader)
        return dict(zip(header, row))

def load_prompt_from_txt(filepath):
     with open(filepath, 'r', encoding='utf-8') as f:
         return f.read()
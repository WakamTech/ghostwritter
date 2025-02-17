import requests
from bs4 import BeautifulSoup
import re

def extract_text_from_url(url):
    """Extrait le texte principal d'une page Web."""
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        # On tente d'extraire le contenu principal en retirant les balises.
        text = ' '.join(p.get_text() for p in soup.find_all('p'))
        text = re.sub(r'\s+', ' ', text).strip() # Supprimer les espaces multiples
        return text
    except Exception:
        return None
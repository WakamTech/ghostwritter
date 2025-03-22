from googlesearch import search
import requests
from bs4 import BeautifulSoup

def get_organic_urls(query, num_results=3, lang='fr', tld='fr'): # Add tld parameter
    """Récupère les URLs de résultats organiques validés."""
    urls = []
    for url in search(query, num=10, stop=10, lang=lang, pause=3, tld=tld): # Use tld parameter
       if not is_ad_url(url) and is_valid_page(url):
           urls.append(url)
           if len(urls) == num_results:
            break
    return urls


def is_ad_url(url):
    """Vérifie si une URL est une publicité."""
    return 'googleadservices.com' in url or 'ads.google.com' in url

def is_valid_page(url):
    """Vérifie si une URL est une page valide."""
    try:
        response = requests.get(url, timeout=60)
        response.raise_for_status()
        if response.headers.get('content-type').startswith('text/html'):
            return True
        else:
            return False
    except Exception:
        return False
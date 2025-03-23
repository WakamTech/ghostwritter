from googlesearch import search
import requests
from bs4 import BeautifulSoup

def get_organic_urls(query, num_results=4):
    """Récupère les URLs de résultats organiques validés."""
    urls = []
    for url in search(query, num=10, stop=10, lang='fr', pause=5, tld="fr"): # chercher plus que 4, et le timeout est à 10, tld=fr
       if not is_ad_url(url) and is_valid_page(url):
           urls.append(url)
           if len(urls) == num_results:
            break # sortez quand on a le nombre de resultat voulu
    return urls


def is_ad_url(url):
    """Vérifie si une URL est une publicité."""
    # Une heuristique simple, à améliorer si nécessaire
    return 'googleadservices.com' in url or 'ads.google.com' in url

def is_valid_page(url):
    """Vérifie si une URL est une page valide."""
    try:
        response = requests.get(url, timeout=60) # Le timeout de la request est à 10
        response.raise_for_status()  # Lève une exception pour les erreurs HTTP
        if response.headers.get('content-type').startswith('text/html'):
            return True
        else:
            return False
    except Exception:
        return False
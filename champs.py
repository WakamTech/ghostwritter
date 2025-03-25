import requests
import json

def get_acf_fields(site_url, post_id, post_type='posts', get_definitions=False):
    """
    Récupère les champs ACF d'un post ou d'une page via l'API REST standard ou une API personnalisée.

    Args:
        site_url: L'URL de base du site WordPress (ex: 'https://example.com').
        post_id: L'ID du post ou de la page.
        post_type: Le type de post ('posts', 'pages', ou un type de post personnalisé).
        get_definitions: Si True, tente de récupérer les définitions des champs ACF (nécessite une API personnalisée).

    Returns:
        Un dictionnaire contenant les champs ACF (valeurs et/ou définitions), ou None si une erreur survient.
    """

    if not site_url.endswith('/'):
        site_url += '/'

    # --- Approche 1: API REST Standard ---
    standard_endpoint = f"{site_url}wp-json/wp/v2/{post_type}/{post_id}"
    try:
        response = requests.get(standard_endpoint)
        response.raise_for_status()
        data = response.json()

        if 'acf' in data:
            acf_data = {'values': data['acf']}  # Initialiser avec les valeurs
            if get_definitions:
              print("Pour obtenir les définitions, une API personnalisée est recommandée (voir l'exemple PHP dans la réponse précédente).")
            return acf_data

    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la requête (API standard) : {e}")
    except json.JSONDecodeError:
        print("Erreur : Réponse JSON invalide (API standard).")

    print("Aucun champ ACF trouvé via l'API REST standard.")


    # --- Approche 2: API REST Personnalisée (si disponible) ---
    #  (Vous devez adapter cette partie si vous avez une API personnalisée)
    if get_definitions:
      custom_endpoint = f"{site_url}wp-json/myplugin/v1/acf-fields/{post_id}" # À ADAPTER
      try:
          response = requests.get(custom_endpoint)
          response.raise_for_status()
          data = response.json()
          return data  # Retourne à la fois 'values' et 'definitions'

      except requests.exceptions.RequestException as e:
          print(f"Erreur lors de la requête (API personnalisée) : {e}")
      except json.JSONDecodeError:
          print("Erreur : Réponse JSON invalide (API personnalisée).")

      print("Aucun champ ACF trouvé via l'API REST personnalisée.")


    # --- Si aucune approche ne fonctionne ---
    return None



def get_all_acf_fields_for_type(site_url, post_type='posts', limit=10, get_definitions=False):
    """
    Récupère les champs ACF pour plusieurs posts/pages d'un même type.

    Args:
        site_url: L'URL de base du site.
        post_type: Le type de post.
        limit: Le nombre maximum de posts à récupérer.
        get_definitions:  Récupérer les définitions (nécessite API personnalisée).

    Returns:
        Une liste de dictionnaires, chacun contenant les champs ACF d'un post.
    """

    if not site_url.endswith('/'):
        site_url += '/'
    endpoint = f"{site_url}wp-json/wp/v2/{post_type}?per_page={limit}"

    try:
        response = requests.get(endpoint)
        response.raise_for_status()
        posts = response.json()

        all_acf_data = []
        for post in posts:
            post_id = post['id']
            acf_data = get_acf_fields(site_url, post_id, post_type, get_definitions)
            if acf_data:
                all_acf_data.append({'post_id': post_id, 'acf': acf_data})

        return all_acf_data

    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la requête (liste de posts) : {e}")
        return None
    except json.JSONDecodeError:
        print("Erreur: Réponse JSON invalide (liste de posts).")
        return None



# --- Exemples d'utilisation ---

site_url = "https://www.havanaonlinecasino.com/"   # REMPLACEZ PAR VOTRE URL
post_id = 32                               # REMPLACEZ PAR UN ID DE POST/PAGE
post_type = "pages"                         # 'posts', 'pages', ou un type personnalisé

# 1. Récupérer les valeurs ACF d'un seul post:
acf_values = get_acf_fields(site_url, post_id, post_type)
if acf_values:
    print("Valeurs ACF:")
    print(json.dumps(acf_values, indent=4))


# 2. Récupérer les valeurs ACF d'un seul post, en essayant aussi l'API custom:
acf_data = get_acf_fields(site_url, post_id, post_type, get_definitions=True)
if acf_data:
    print("\nDonnées ACF (valeurs et/ou définitions):")
    print(json.dumps(acf_data, indent=4))

# 3. Récupérer les valeurs ACF pour plusieurs posts (ex: les 5 premiers posts):
all_acf = get_all_acf_fields_for_type(site_url, post_type="posts", limit=5)
if all_acf:
    print("\nValeurs ACF pour plusieurs posts:")
    print(json.dumps(all_acf, indent=4))


# 4. Récupérer les valeurs ET définitions pour plusieurs posts (API personnalisée):
all_acf_with_definitions = get_all_acf_fields_for_type(site_url, post_type="posts", limit=5, get_definitions=True)
if all_acf_with_definitions:
    print("\nDonnées ACF (valeurs et définitions) pour plusieurs posts:")
    print(json.dumps(all_acf_with_definitions, indent=4))

# 5. Exemple avec un type de post personnalisé:
custom_post_type = "produits"  # REMPLACEZ par votre type de post personnalisé
custom_post_id = 456 # ID d'un post de ce type
custom_acf = get_acf_fields(site_url, custom_post_id, custom_post_type, get_definitions=True)
if custom_acf:
    print(f"\nACF pour le type personnalisé '{custom_post_type}':")
    print(json.dumps(custom_acf, indent=4))

# 6.  Récupérer les champs pour TOUS les posts d'un type (attention à la performance!):
# all_acf_for_all_posts = get_all_acf_fields_for_type(site_url, post_type="posts", limit=100)  # Augmentez 'limit' si besoin, mais soyez prudent!
# if all_acf_for_all_posts:
#     print(json.dumps(all_acf_for_all_posts, indent=4))
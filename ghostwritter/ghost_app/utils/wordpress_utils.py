# wordpress_utils.py
import requests
import json # Importer json pour le débogage Yoast (si nécessaire)
from urllib.parse import urlparse
# Retirer les imports xmlrpc si plus utilisés
# from wordpress_xmlrpc import Client, WordPressPost
# from wordpress_xmlrpc.methods.posts import NewPost, GetPosts

# Liste des clés ACF potentielles à vérifier lors de la mise à jour
POSSIBLE_ACF_MESSAGES_KEYS = [
    'main_content', 'vision', 'faqs', 'meta_description', 'promotion',
    'slots_description', 'short_description', 'page_title', 'introduction',
    'playing_with_crypto', 'contact_details', 'faqs_1', 'faqs_2', 'faqs_3',
    'faqs_4', 'faqs_5', 'faqs_6', 'glossary_1', 'glossary_2', 'glossary_3',
    'glossary_test', 'news_1', 'news_2', 'news_3', 'terms', 'meta_title' # meta_title ajouté ici aussi
]

def get_post_data(post_id, wordpress_url, username, password, post_type='page'):
    """Retrieves full post/page data by ID using the REST API."""
    print(f"get_post_data called for post_id: {post_id}, type: {post_type}")
    try:
        endpoint = f"{post_type}s" # pages or posts
        api_url = f"{wordpress_url.rstrip('/')}/wp-json/wp/v2/{endpoint}/{post_id}?context=edit" # context=edit pour obtenir toutes les données ACF/meta si possible
        print(f"API URL for get_post_data: {api_url}")

        response = requests.get(api_url, auth=(username, password))
        response.raise_for_status()
        post_data = response.json()
        print(f"get_post_data raw response for ID {post_id}: {json.dumps(post_data, indent=2)}") # Debug print full response

        # Vérifions si acf_messages est présent (au cas où il ne serait pas renvoyé)
        if 'acf_messages' not in post_data:
             print(f"WARNING: 'acf_messages' field not found in the response for post ID {post_id}. Assuming empty.")
             post_data['acf_messages'] = [] # Retourner une liste vide si non trouvé

        # Vérifions également acf (au cas où les champs seraient sous 'acf')
        if 'acf' not in post_data:
            print(f"WARNING: 'acf' field not found in the response for post ID {post_id}. Assuming empty.")
            post_data['acf'] = {} # Retourner un dict vide si non trouvé

        return post_data # Return the entire post object

    except requests.exceptions.RequestException as e:
        # Gérer spécifiquement les 404 (Not Found)
        if e.response is not None and e.response.status_code == 404:
            print(f"Error 404: Post/Page with ID {post_id} and type '{post_type}' not found at {api_url}.")
        else:
            print(f"HTTP Request Error in get_post_data: {e}")
            if e.response is not None:
                print(f"Response status code: {e.response.status_code}")
                print(f"Response text: {e.response.text}")
        return None
    except Exception as e:
        print(f"Erreur lors de la récupération des données du post/page {post_id}: {e}")
        return None

# Simplification: Ces fonctions acceptent maintenant un dict 'data' complet
def create_wordpress_resource(data, wordpress_url, username, password, post_type='page'):
    """Creates a new WordPress resource (post/page) using the REST API."""
    print(f"create_wordpress_resource called with type: {post_type}")
    try:
        endpoint = f"{post_type}s" # pages or posts
        api_url = f"{wordpress_url.rstrip('/')}/wp-json/wp/v2/{endpoint}"
        print(f"API URL for create: {api_url}")
        print(f"--- Data being sent for CREATE ---")
        print(json.dumps(data, indent=2)) # Log data being sent
        print(f"----------------------------------")


        response = requests.post(api_url, auth=(username, password), json=data)

        # Log response status and content regardless of success/failure initially
        print(f"Create Response Status Code: {response.status_code}")
        try:
            response_json = response.json()
            print("--- Create Response Content ---")
            print(json.dumps(response_json, indent=2))
            print("-----------------------------")
        except json.JSONDecodeError:
            print("--- Create Response Content (Not JSON) ---")
            print(response.text)
            print("-----------------------------------------")

        response.raise_for_status() # Raise exception for bad status codes (4xx or 5xx)
        post_data = response.json()
        return post_data['id'] # Return the new post ID

    except requests.exceptions.RequestException as e:
        print(f"HTTP Request Error (create): {e}")
        # More detailed error logging already happened above
        return None
    except Exception as e:
        print(f"Error during resource creation: {e}")
        return None

def update_wordpress_resource(post_id, data, wordpress_url, username, password, post_type='page'):
    """Updates an existing WordPress resource (post/page) using the REST API."""
    print(f"update_wordpress_resource called for post_id: {post_id}, type: {post_type}")
    try:
        endpoint = f"{post_type}s" # pages or posts
        api_url = f"{wordpress_url.rstrip('/')}/wp-json/wp/v2/{endpoint}/{post_id}"
        print(f"API URL for update: {api_url}")
        print(f"--- Data being sent for UPDATE (ID: {post_id}) ---")
        print(json.dumps(data, indent=2)) # Log data being sent
        print(f"-------------------------------------------")

        # Utiliser requests.post ou requests.put - POST est souvent utilisé pour les mises à jour partielles dans WP REST API
        response = requests.post(api_url, auth=(username, password), json=data)

        # Log response status and content
        print(f"Update Response Status Code: {response.status_code}")
        try:
            response_json = response.json()
            print("--- Update Response Content ---")
            print(json.dumps(response_json, indent=2))
            print("-----------------------------")
        except json.JSONDecodeError:
            print("--- Update Response Content (Not JSON) ---")
            print(response.text)
            print("-----------------------------------------")


        response.raise_for_status()
        return True

    except requests.exceptions.RequestException as e:
        print(f"HTTP Request Error (update): {e}")
        # More detailed error logging already happened above
        return False
    except Exception as e:
        print(f"Erreur lors de la mise à jour de la ressource {post_id}: {e}")
        return False

# --- Fonctions existantes modifiées ou à vérifier ---

def get_post_id_from_slug(wordpress_url, username, password, slug, post_type='page'):
    """Gets post/page ID from slug, prioritizing the specified post_type (default 'page')."""
    print(f"get_post_id_from_slug called for slug: '{slug}', checking type: '{post_type}' first")
    types_to_check = [post_type] + ([t for t in ['page', 'post'] if t != post_type]) # Check specified type first

    for current_type in types_to_check:
        try:
            endpoint = f"{current_type}s" # pages or posts
            api_url = f"{wordpress_url.rstrip('/')}/wp-json/wp/v2/{endpoint}?slug={slug}&status=any" # status=any pour trouver brouillons etc.
            print(f"API URL for get_post_id_from_slug ({current_type}): {api_url}")

            response = requests.get(api_url, auth=(username, password))
            response.raise_for_status()
            posts = response.json()

            if posts:
                if len(posts) > 1:
                    print(f"Multiple {current_type}s found with slug '{slug}'. Using the first one (ID: {posts[0]['id']}).")
                print(f"Found {current_type} with ID: {posts[0]['id']} for slug '{slug}'")
                return posts[0]['id'], current_type # Return ID and the type it was found as

        except requests.exceptions.RequestException as e:
            # Ignore 404s here as we might find it in the other type
            if e.response is not None and e.response.status_code == 404:
                 print(f"No {current_type} found with slug '{slug}'.")
            else:
                print(f"HTTP Request Error in get_post_id_from_slug ({current_type}): {e}")
        except Exception as e:
            print(f"Error in get_post_id_from_slug ({current_type}): {e}")

    print(f"No post or page found for slug '{slug}' after checking both types.")
    return None, None # Return None for both ID and type if not found

def get_home_page_id(wordpress_url, username, password):
    """Retrieves the ID of the WordPress home page (static front page) using the REST API."""
    print("Attempting to get home page ID...")
    try:
        api_url = f"{wordpress_url.rstrip('/')}/wp-json/wp/v2/settings"
        response = requests.get(api_url, auth=(username, password))
        response.raise_for_status()
        settings = response.json()
        print("WP Settings received:", settings) # Debug print
        if settings.get('show_on_front') == 'page':
            page_id = settings.get('page_on_front')
            if page_id and page_id != 0: # Ensure it's a valid ID
                 print(f"Static front page detected. ID: {page_id}")
                 return page_id
            else:
                 print("Setting 'show_on_front' is 'page', but 'page_on_front' is missing or 0.")
        else:
            print(f"Setting 'show_on_front' is '{settings.get('show_on_front', 'not set')}'. Not a static page.")
        return None
    except requests.exceptions.RequestException as e:
        print(f"HTTP Request Error (get_home_page_id): {e}")
        return None
    except Exception as e:
        print(f"Error getting home page ID: {e}")
        return None

# --- Fonction create_or_update n'est plus vraiment nécessaire si la logique est dans views.py ---
# Mais on peut la garder pour appeler les nouvelles fonctions simplifiées
def create_or_update_wordpress_resource(data, wordpress_url, username, password, post_id=None, post_type='page'):
    """Creates or updates a WordPress resource using the simplified functions."""
    if post_id:
        print(f"Calling update_wordpress_resource for ID: {post_id}")
        return update_wordpress_resource(post_id, data, wordpress_url, username, password, post_type)
    else:
        print(f"Calling create_wordpress_resource")
        # create_wordpress_resource returns the new ID on success, or None on failure
        new_id = create_wordpress_resource(data, wordpress_url, username, password, post_type)
        return new_id # Return the ID or None
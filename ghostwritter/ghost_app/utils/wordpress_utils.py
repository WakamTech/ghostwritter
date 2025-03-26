import requests
from urllib.parse import urlparse
from wordpress_xmlrpc import Client, WordPressPost  # Keep this for potential backward compatibility if needed
from wordpress_xmlrpc.methods.posts import NewPost, GetPosts


def create_wordpress_post(title, content, wordpress_url, username, password, post_status='draft', post_type='post', meta_title=None, meta_description=None):
    """Creates a new WordPress post using the REST API."""
    # print(f"create_wordpress_post called with title: {title}, post_type: {post_type}, post_status: {post_status}")  # Debug print
    try:
        # Construct the correct endpoint based on post_type
        endpoint = 'pages' if post_type == 'page' else 'posts'
        api_url = f"{wordpress_url.rstrip('/')}/wp-json/wp/v2/{endpoint}"
        # print(f"API URL for create: {api_url}")  # Debug print

        data = {
            'title': title,
            'content': content,
            'status': post_status,  # Use the provided post_status
        }

        # Add Yoast SEO fields if provided
        if meta_title:
            data['_yoast_wpseo_title'] = meta_title
        if meta_description:
            data['_yoast_wpseo_metadesc'] = meta_description

        response = requests.post(api_url, auth=(username, password), json=data)
        response.raise_for_status()
        post_data = response.json()
        # print(f"create_wordpress_post response: {post_data}")  # Debug print
        return post_data['id']  # Return the new post ID

    except requests.exceptions.RequestException as e:
        print(f"HTTP Request Error (create): {e}")
        return None
    except Exception as e:
        print(f"Error during post creation: {e}")
        return None


def get_post_by_url(post_url, wordpress_url, username, password):
    """Retrieves a WordPress post by its URL using the REST API and checks Yoast SEO data."""
    print(f"get_post_by_url called with post_url: {post_url}")
    try:
        parsed_url = urlparse(post_url)
        path_parts = parsed_url.path.split('/')
        slug = next((part for part in reversed(path_parts) if part), None)

        if not slug:
            print(f"Impossible d'extraire le slug de l'URL : {post_url}")
            return None

        api_url = f"{wordpress_url.rstrip('/')}/wp-json/wp/v2/posts?slug={slug}"
        print(f"API URL for get_post_by_url: {api_url}")

        response = requests.get(api_url, auth=(username, password))
        response.raise_for_status()
        posts = response.json()
        print(f"get_post_by_url response: {posts}")

        if not posts:
            print(f"Aucun article trouvé avec le slug : {slug}")
            return None
        elif len(posts) > 1:
            print(f"Attention: Plusieurs articles trouvés avec le slug: {slug}. Le premier sera utilisé.")
        post = posts[0]  # Take the first post

        # **Retrieve Yoast SEO data**
        post_id = post['id']
        api_url_single_post = f"{wordpress_url.rstrip('/')}/wp-json/wp/v2/posts/{post_id}"
        response_single_post = requests.get(api_url_single_post, auth=(username, password))
        response_single_post.raise_for_status()
        post_data = response_single_post.json()

        if 'yoast_head_json' in post_data:
            yoast_data = post_data['yoast_head_json']
            print("Yoast SEO Data:", json.dumps(yoast_data, indent=2)) # Log Yoast data
        else:
            print("Yoast SEO data not found for this post.")

        print(f"Returning post ID: {post['id']}")
        return post  # Return the entire post object

    except requests.exceptions.RequestException as e:
        print(f"HTTP Request Error: {e}")
        return None
    except Exception as e:
        print(f"Erreur lors de la récupération de l'article : {e}")
        return None

def update_wordpress_post(post_id, title, content, wordpress_url, username, password, post_status='publish', post_type='post', meta_title=None, meta_description=None):
    """Met à jour un article WordPress existant en utilisant l'API REST."""
    print(f"update_wordpress_post called with post_id: {post_id}, post_type: {post_type}")
    try:
        endpoint = 'pages' if post_type == 'page' else 'posts'
        api_url = f"{wordpress_url.rstrip('/')}/wp-json/wp/v2/{endpoint}/{post_id}"
        print(f"API URL for update: {api_url}")

        data = {
            'title': title,
            'content': content,
            'status': post_status
        }

        # Add Yoast SEO fields if provided
        if meta_title:
            data['_yoast_wpseo_title'] = meta_title
        if meta_description:
            data['_yoast_wpseo_metadesc'] = meta_description

        response = requests.post(api_url, auth=(username, password), json=data)
        response.raise_for_status()
        # print(f"update_wordpress_post response: {response.json()}")
        return True

    except requests.exceptions.RequestException as e:
        print(f"HTTP Request Error: {e}")
        return False
    except Exception as e:
        print(f"Erreur lors de la mise à jour de l'article : {e}")
        return False

def create_or_update_wordpress_post(title, content, wordpress_url, username, password, post_status='draft', post_id=None, post_type='post', meta_title=None, meta_description=None):
    """Creates or updates a WordPress post/page (using REST API for updates)."""
    if post_id:
        return update_wordpress_post(post_id, title, content, wordpress_url, username, password, post_status, post_type, meta_title, meta_description)
    else:
        return create_wordpress_post(title, content, wordpress_url, username, password, post_status, post_type, meta_title, meta_description) # Use REST API create

def get_post_id_from_slug(wordpress_url, username, password, slug, post_type='page'):
    """get_post_id_from_slug (using REST API)"""
    try:
        api_url = f"{wordpress_url.rstrip('/')}/wp-json/wp/v2/{post_type}s?slug={slug}"
        response = requests.get(api_url, auth=(username, password))
        response.raise_for_status()
        posts = response.json()

        if not posts:
            return None
        elif len(posts) > 1:
             print(f"Multiple {post_type}s found with slug '{slug}'. Using the first one.")
        return posts[0]['id']

    except requests.exceptions.RequestException as e:
        print(f"HTTP Request Error in get_post_id_from_slug: {e}")
        return None
    except Exception as e:
        print(f"Error in get_post_id_from_slug: {e}")
        return None

# In your wordpress_utils.py (add this function)

def get_home_page_id(wordpress_url, username, password):
    """Retrieves the ID of the WordPress home page (static front page) using the REST API."""
    try:
        api_url = f"{wordpress_url.rstrip('/')}/wp-json/wp/v2/settings"
        response = requests.get(api_url, auth=(username, password))
        response.raise_for_status()
        settings = response.json()
        # print(settings) # Debug print
        if 'show_on_front' in settings and settings['show_on_front'] == 'page':
            if 'page_on_front' in settings:
                return settings['page_on_front']
        return None  # No static front page set or 'show_on_front' is not 'page'
    except requests.exceptions.RequestException as e:
        print(f"HTTP Request Error (get_home_page_id): {e}")
        return None
    except Exception as e:
        print(f"Error getting home page ID: {e}")
        return None
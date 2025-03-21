from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost, EditPost, GetPosts
import time
import csv
import re
from urllib.parse import urljoin, urlparse
from config_utils import load_config_from_csv, load_prompt_from_txt
from google_search import get_organic_urls
from content_extractor import extract_text_from_url
from openai_utils import generate_article, generate_summary_table, generate_title
from markdown_to_html import markdown_to_html

def update_wordpress_post(post_id, title, content, wordpress_url, username, password):
    """Met à jour un post ou une page WordPress existante."""
    try:
        client = Client(wordpress_url, username, password)
        post = WordPressPost()
        post.title = title
        post.content = content
        success = client.call(EditPost(post_id, post))
        return success
    except Exception as e:
        print(f"Erreur lors de la mise à jour du post WordPress : {e}")
        return False

def create_or_update_wordpress_post(title, content, wordpress_url, username, password, post_status='draft', post_id=None, post_type='post'):
    """Crée ou met à jour un article ou une page WordPress."""
    try:
        client = Client(wordpress_url, username, password)
        post = WordPressPost()
        post.title = title
        post.content = content
        post.post_status = 'publish'  # Toujours publier

        if post_id:  # Mise à jour d'un contenu existant
            existing_post = client.call(GetPosts({'include': [post_id]}))[0]
            if existing_post.post_type != post_type:
                print(f"Erreur : Impossible de changer le type '{existing_post.post_type}' en '{post_type}'.")
                return False

            success = client.call(EditPost(post_id, post))
            return success
        else:  # Création d'un nouveau contenu
            post.post_status = post_status
            post.post_type = post_type
            new_post_id = client.call(NewPost(post))
            return new_post_id

    except Exception as e:
        print(f"Erreur lors de la création ou mise à jour du post WordPress : {e}")
        return None

def get_post_id_from_slug(wordpress_url, username, password, slug, post_type='page'):
    """Récupère l'ID d'un post ou d'une page à partir de son slug."""
    try:
        client = Client(wordpress_url, username, password)
        posts = client.call(GetPosts({'post_type': post_type, 'number': 10000, 'orderby': 'ID'}))
        for post in posts:
            if post.slug == slug:
                return post.id
        return None
    except Exception as e:
        print(f"Erreur lors de la récupération de l'ID à partir du slug : {e}")
        return None

def main():
    """Orchestre le processus principal."""
    openai_credentials = load_config_from_csv('credentials_openai.csv')
    wordpress_credentials = load_config_from_csv('credentials_wordpress.csv')
    general_config = load_config_from_csv('config.csv')
    prompt_article_v1 = load_prompt_from_txt('prompt_article_v1.txt')
    prompt_article_v2 = load_prompt_from_txt('prompt_article_v2.txt')
    prompt_resume = load_prompt_from_txt('prompt_resume.txt')

    with open('sites_keywords.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  # Ignore l'en-tête

        for row in reader:
            provided_url, query = row
            print(f"Processing URL: {provided_url}, keyword: {query}")

            try:
                # Déterminer le type d'URL et récupérer l'ID du post
                parsed_url = urlparse(provided_url)
                base_url = parsed_url.scheme + "://" + parsed_url.netloc
                full_wordpress_url = urljoin(base_url, 'xmlrpc.php')

                post_id = None
                post_type = 'post'

                if parsed_url.path and parsed_url.path != '/' and 'xmlrpc.php' not in parsed_url.path:
                    slug = parsed_url.path.strip('/')

                    post_id = get_post_id_from_slug(full_wordpress_url, wordpress_credentials['username'], wordpress_credentials['password'], slug, post_type='page')
                    if post_id:
                        post_type = 'page'
                    else:
                        post_id = get_post_id_from_slug(full_wordpress_url, wordpress_credentials['username'], wordpress_credentials['password'], slug, post_type='post')

                # Génération de l'article
                if general_config['generation_mode'] == 'search':
                    urls = get_organic_urls(query, num_results=int(general_config['num_results']), lang=general_config['search_language'], tld=general_config['search_domain'])

                    if not urls:
                        print(f"Aucun résultat trouvé pour : {query}")
                        continue

                    all_text = ""
                    for url in urls:
                        text = extract_text_from_url(url)
                        if text:
                            all_text += f" {text}"

                    article = generate_article(prompt_article_v1, all_text, openai_credentials['api_key'], query, openai_credentials['model'])

                elif general_config['generation_mode'] == 'direct':
                    article = generate_article(prompt_article_v2, "", openai_credentials['api_key'], query, openai_credentials['model'])

                else:
                    print(f"Mode de génération invalide : {general_config['generation_mode']}")
                    continue

                if not article:
                    print("Erreur lors de la génération de l'article")
                    continue

                title = generate_title("Génère un titre percutant pour cet article", article, openai_credentials['api_key'], openai_credentials['model'])
                if not title:
                    print("Erreur lors de la génération du titre")
                    continue

                title = title.strip('"«»')
                summary = generate_summary_table(prompt_resume, article, openai_credentials['api_key'], openai_credentials['model'])

                article = markdown_to_html(article)
                full_content = f"<p>{summary}</p><p>{article}</p>"

                result = create_or_update_wordpress_post(title, full_content, full_wordpress_url,
                                                        wordpress_credentials['username'], wordpress_credentials['password'],
                                                        post_status=general_config['post_status'], post_id=post_id, post_type=post_type)

                if result:
                    action = "mis à jour" if post_id else "créé"
                    print(f"Article {action} avec succès : ID = {result}")
                else:
                    print("Échec de la création ou de la mise à jour de l'article.")

                time.sleep(3)

            except Exception as e:
                print(f"Erreur lors du traitement de l'URL {provided_url}, keyword {query} : {e}")
                continue

if __name__ == "__main__":
    main()

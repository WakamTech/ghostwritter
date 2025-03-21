import time
import csv
from urllib.parse import urljoin, urlparse
from config_utils import load_config_from_csv, load_prompt_from_txt
from google_search import get_organic_urls
from content_extractor import extract_text_from_url
from openai_utils import generate_article, generate_summary_table, generate_title
from wordpress_utils import create_or_update_wordpress_post, get_post_id_from_slug
from markdown_to_html import markdown_to_html

def main():
    """Orchestrates the main process."""

    openai_credentials = load_config_from_csv('credentials_openai.csv')
    wordpress_credentials = load_config_from_csv('credentials_wordpress.csv')
    general_config = load_config_from_csv('config.csv')
    prompt_article_v1 = load_prompt_from_txt('prompt_article_v1.txt')
    prompt_article_v2 = load_prompt_from_txt('prompt_article_v2.txt')
    prompt_resume = load_prompt_from_txt('prompt_resume.txt')

    with open('sites_keywords.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header row

        for row in reader:
            provided_url, query = row
            print(f"Processing URL: {provided_url}, keyword: {query}")

            try:
                # --- Determine URL Type and Get Post ID ---
                parsed_url = urlparse(provided_url)
                base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
                # Use base_url for the REST API (no xmlrpc.php)
                full_wordpress_url = base_url
                print(f"Full WordPress URL: {full_wordpress_url}")

                if parsed_url.path and parsed_url.path != '/' and 'xmlrpc.php' not in parsed_url.path:
                    slug = parsed_url.path.strip('/')
                    print(f"Slug: {slug}")

                    # Check for page first, then post
                    post_id = get_post_id_from_slug(full_wordpress_url, wordpress_credentials['username'], wordpress_credentials['password'], slug, post_type='page')
                    # print(f"Initial post_id (checking for page): {post_id}")

                    if post_id:
                        post_type = 'page'
                    else:
                        post_id = get_post_id_from_slug(full_wordpress_url, wordpress_credentials['username'], wordpress_credentials['password'], slug, post_type='post')
                        # print(f"post_id (checking for post): {post_id}")
                        post_type = 'post' if post_id else None

                    if not post_id:
                        print(f"No post or page found with slug '{slug}' on {full_wordpress_url}. Creating a new post.")
                        post_type = 'post'  # Default to 'post' for new content

                else:  # It's a base URL or something unexpected.  Create a new post.
                    post_id = None
                    post_type = 'post' # Default to post type 'post'

                # print(f"Final post_id: {post_id}, post_type: {post_type}")  # VERY IMPORTANT


                # --- Generate Article (rest of the article generation code) ---
                if general_config['generation_mode'] == 'search':
                    urls = get_organic_urls(query, num_results=int(general_config['num_results']), lang=general_config['search_language'], tld=general_config['search_domain'])
                    if not urls:
                        print(f"No valid search results for: {query}")
                        continue

                    all_text = "".join([extract_text_from_url(url) or "" for url in urls])
                    article = generate_article(prompt_article_v1, all_text, openai_credentials['api_key'], query, openai_credentials['model'])

                elif general_config['generation_mode'] == 'direct':
                    article = generate_article(prompt_article_v2, "", openai_credentials['api_key'], query, openai_credentials['model'])

                else:
                    print(f"Invalid generation_mode: {general_config['generation_mode']}")
                    continue

                if not article:
                    print("Error generating article")
                    continue

                title = generate_title("Génère un titre percutant pour cet article", article, openai_credentials['api_key'], openai_credentials['model']).strip('"').strip('«').strip('»')
                summary = generate_summary_table(prompt_resume, article, openai_credentials['api_key'], openai_credentials['model'])

                if not title or not summary:
                    print("Error generating title or summary")
                    continue

                article = markdown_to_html(article)
                full_content = f"<p>{summary}</p><p>{article}</p>"

                # --- Determine Post Status ---
                if post_id:
                    current_post_status = 'publish'  # Force publish for updates
                else:
                    current_post_status = general_config['post_status']  # Use config for new posts
                # print(f"Current post_status {current_post_status}")
                # --- Create or Update Post ---
                # print(f"Calling create_or_update_wordpress_post with post_id: {post_id}, post_type: {post_type}, post_status: {current_post_status}")
                result = create_or_update_wordpress_post(
                    title,
                    full_content,
                    full_wordpress_url,  # Now using base URL
                    wordpress_credentials['username'],
                    wordpress_credentials['password'],
                    post_status=current_post_status,
                    post_id=post_id,
                    post_type=post_type  # Still pass post_type for consistency
                )

                if result:
                    if post_id:
                        print(f"Article/Page updated successfully on {full_wordpress_url} with Post ID: {post_id}")
                    else:
                        print(f"Article created with ID: {result} on {full_wordpress_url}")
                else:
                    print("Failed to create or update article.")

                time.sleep(3)  # Be nice to the API

            except Exception as e:
                print(f"Error processing URL {provided_url}, keyword {query}: {e}")
                print("Moving to the next entry...")

if __name__ == "__main__":
    main()
import time
import csv
import re
from urllib.parse import urljoin
from config_utils import load_config_from_csv, load_prompt_from_txt
# from google_search import get_organic_urls  # REMOVE
# from content_extractor import extract_text_from_url  # REMOVE
from openai_utils import generate_article, generate_summary_table, generate_title
from wordpress_utils import create_wordpress_draft
from markdown_to_html import markdown_to_html

def main():
    """Orchestrates the main process for multiple sites."""

    openai_credentials = load_config_from_csv('credentials_openai.csv')
    wordpress_credentials = load_config_from_csv('credentials_wordpress.csv')
    prompt_article = load_prompt_from_txt('prompt_article.txt')
    prompt_resume = load_prompt_from_txt('prompt_resume.txt')

    with open('sites_keywords.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)

        for row in reader:
            site_url, query = row
            full_wordpress_url = urljoin(site_url, 'xmlrpc.php')
            print(f"Processing site: {site_url}, keyword: {query}")
            print(f"Full WordPress URL: {full_wordpress_url}")

            article = None  # Initialize for error handling
            try:
                # --- REMOVE Google Search and Content Extraction ---
                # urls = get_organic_urls(query)
                # if not urls:
                #     print(f"No valid search results for: {query} on {site_url}")
                #     continue

                # all_text = ""
                # for url in urls:
                #     text = extract_text_from_url(url)
                #     if text:
                #         all_text += f" {text}"

                # --- Generate Article Directly from Prompt and Query ---
                article = generate_article(prompt_article, "", openai_credentials['api_key'], query, openai_credentials['model']) # Pass empty string for content
                if not article:
                    print(f"Error generating article for {query} on {site_url}")
                    continue

                title_prompt = "Génère un titre percutant pour cet article"
                title = generate_title(title_prompt, article, openai_credentials['api_key'], openai_credentials['model'])
                if not title:
                    print(f"Error generating title for {query} on {site_url}")
                    continue

                title = title.strip('"').strip('«').strip('»')

                summary = generate_summary_table(prompt_resume, article, openai_credentials['api_key'], openai_credentials['model'])
                if not summary:
                    print(f"Error generating summary for {query} on {site_url}")
                    continue

                article = markdown_to_html(article) # Keep this line!  This is now CORRECT.
                full_content = f"<p>{summary}</p><p>{article}</p>"

                post_id = create_wordpress_draft(title, full_content,
                                                full_wordpress_url,
                                                wordpress_credentials['username'],
                                                wordpress_credentials['password'])
                if post_id:
                    print(f"Article published with ID: {post_id} on {full_wordpress_url}")

                time.sleep(300)

            except Exception as e:
                print(f"Error processing site {site_url}, keyword {query}: {e}")
                print("Moving to the next entry...")
                continue

if __name__ == "__main__":
    main()
import time
import csv
import re
from config_utils import load_config_from_csv, load_prompt_from_txt
from google_search import get_organic_urls
from content_extractor import extract_text_from_url
from openai_utils import generate_article, generate_summary_table, generate_title
from wordpress_utils import create_wordpress_draft
from markdown_to_html import markdown_to_html


def main():
    """Orchestre le processus principal."""
    
    # Chargement des configurations
    openai_credentials = load_config_from_csv('credentials_openai.csv')
    wordpress_credentials = load_config_from_csv('credentials_wordpress.csv')
    prompt_article = load_prompt_from_txt('prompt_article.txt')
    prompt_resume = load_prompt_from_txt('prompt_resume.txt')

    with open('requetes.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            query = row[0]  # Assumons une seule requête par ligne
            print(f"Traitement de la requête: {query}")
            try:
                # 1. Recherche sur Google et validation des URL
                urls = get_organic_urls(query)
                if not urls:
                    print(f"Aucun résultat de recherche valide pour : {query}")
                    continue
                
                # 2. Extraction du texte
                all_text = ""
                for url in urls:
                    text = extract_text_from_url(url)
                    if text:
                        all_text += f" {text}"

                # 3. Génération de l'article avec OpenAI
                article = generate_article(prompt_article, all_text, openai_credentials['api_key'], query, openai_credentials['model'])

                if not article:
                    print(f"Erreur pendant la generation de l'article")
                    continue

                # 4. Génération du titre
                title_prompt = "Génère un titre percutant pour cet article. Retourne juste directement le titre, pas de phase d'introduction ou de conclusion, absolument rien d'autres. Retourne le titre directemment sans aucune miseen forme juste un simple texte"
                title = generate_title(title_prompt, article, openai_credentials['api_key'], openai_credentials['model'])

                if not title:
                    print(f"Erreur pendant la generation du titre")
                    continue
                
                # 4.1 Supprimer les "" du titre s'ils existent
                title = title.strip('"')
                title = title.strip('«')
                title = title.strip('»')

                # 5. Génération du résumé
                summary = generate_summary_table(prompt_resume, article, openai_credentials['api_key'], openai_credentials['model'])
                if not summary:
                    print(f"Erreur pendant la generation du resume")
                    continue

                # 5.1 Convertir le markdown en html
                article = markdown_to_html(article)

                # 6. Publication sur WordPress
                full_content = f"<p>{summary}</p><p>{article}</p>"
                post_id = create_wordpress_draft(title, full_content,
                                            wordpress_credentials['wordpress_url'],
                                            wordpress_credentials['username'],
                                            wordpress_credentials['password'])
                if post_id:
                    print(f"Article publié avec l'ID: {post_id}")
                
                # Pause de 5 minutes
                time.sleep(300)


            except Exception as e:
                print(f"Erreur lors du traitement de la requête {query}: {e}")
                print("Passage à la requête suivante...")
                continue # On passe a la requete suivante
                

if __name__ == "__main__":
    main()
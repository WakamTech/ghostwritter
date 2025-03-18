import openai
import re

def generate_text(prompt, api_key, model):
    """Génère du texte à l'aide de l'API OpenAI."""
    client = openai.OpenAI(api_key=api_key)
    try:
        response = client.chat.completions.create(
        model=model,
        messages=[
                {"role": "user", "content": prompt},
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
      print(f"Erreur dans l'appel de l'api OpenAI: {e}")
      return None

def generate_article(prompt, content, api_key, topic, model):
    """Génère un article à partir d'un prompt et du sujet."""
    # Construct the final prompt, incorporating the topic
    final_prompt = f"{prompt}\n\nSujet de l'article : {topic}"

    article = generate_text(final_prompt, api_key, model)

    if not article:  # Handle potential None return
        return None
    # Extraction du HTML si présent
    html_match = re.search(r'```html(.*?)```', article, re.DOTALL)
    if html_match:
        return html_match.group(1).strip()

    return article  # Return the raw Markdown text


def generate_title(prompt, article, api_key, model):
   """Génère un titre à partir d'un prompt et d'un article."""
   final_prompt = f"{prompt}\n\n{article}"
   return generate_text(final_prompt, api_key, model)


def generate_summary_table(prompt, article, api_key, model):
    """Génère un résumé sous forme de tableau à partir d'un prompt et d'un article.
    On retourne du markdown
    """
    final_prompt = f"{prompt}\n\n{article}"
    summary = generate_text(final_prompt, api_key, model)
    # Extraction du HTML si présent
    html_match = re.search(r'```html(.*?)```', summary, re.DOTALL)
    if html_match:
        return html_match.group(1).strip()
    return summary
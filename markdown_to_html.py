import re

def markdown_to_html(markdown_text):
    """Convertit un texte Markdown en HTML."""
    # Conversion des titres (h1 à h6)
    markdown_text = re.sub(r'^# (.*)$', r'<h1>\1</h1>', markdown_text, flags=re.MULTILINE)
    markdown_text = re.sub(r'^## (.*)$', r'<h2>\1</h2>', markdown_text, flags=re.MULTILINE)
    markdown_text = re.sub(r'^### (.*)$', r'<h3>\1</h3>', markdown_text, flags=re.MULTILINE)
    markdown_text = re.sub(r'^#### (.*)$', r'<h4>\1</h4>', markdown_text, flags=re.MULTILINE)
    markdown_text = re.sub(r'^##### (.*)$', r'<h5>\1</h5>', markdown_text, flags=re.MULTILINE)
    markdown_text = re.sub(r'^###### (.*)$', r'<h6>\1</h6>', markdown_text, flags=re.MULTILINE)
    
    # Conversion des paragraphes
    markdown_text = re.sub(r'^([^#\n]+)$', r'<p>\1</p>', markdown_text, flags=re.MULTILINE)

    # Conversion des listes (ul et ol)
    markdown_text = re.sub(r'^\* (.*)$', r'<li>\1</li>', markdown_text, flags=re.MULTILINE)
    markdown_text = re.sub(r'^[0-9]+\. (.*)$', r'<li>\1</li>', markdown_text, flags=re.MULTILINE)
    markdown_text = re.sub(r'^(<li>.*?</li>(\n|$))+', r'<ul>\n\g<0>\n</ul>', markdown_text, flags=re.MULTILINE)
    markdown_text = re.sub(r'^<ul>(\n*<li>.*?</li>\n*)</ul>', r'<ul>\g<1></ul>', markdown_text, flags=re.MULTILINE)
    
    # Conversion du texte en gras (**)
    markdown_text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', markdown_text)
    
      # Conversion des italiques (*)
    markdown_text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', markdown_text)
    
    # Suppression des espaces multiples
    markdown_text = re.sub(r'\s+', ' ', markdown_text).strip()
    
    # Supprimer les lignes vides
    markdown_text = re.sub(r'^\s*$', '', markdown_text, flags=re.MULTILINE)
    markdown_text = re.sub(r'\n{2,}', '\n', markdown_text)

    return markdown_text
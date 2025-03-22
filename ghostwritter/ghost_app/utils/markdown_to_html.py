import re

def markdown_to_html(markdown_text):
    """Convertit un texte Markdown en HTML."""

    # --- 1. Headings --- (Order doesn't matter much here)
    markdown_text = re.sub(r'^# (.*)$', r'<h1>\1</h1>', markdown_text, flags=re.MULTILINE)
    markdown_text = re.sub(r'^## (.*)$', r'<h2>\1</h2>', markdown_text, flags=re.MULTILINE)
    markdown_text = re.sub(r'^### (.*)$', r'<h3>\1</h3>', markdown_text, flags=re.MULTILINE)
    markdown_text = re.sub(r'^#### (.*)$', r'<h4>\1</h4>', markdown_text, flags=re.MULTILINE)
    markdown_text = re.sub(r'^##### (.*)$', r'<h5>\1</h5>', markdown_text, flags=re.MULTILINE)
    markdown_text = re.sub(r'^###### (.*)$', r'<h6>\1</h6>', markdown_text, flags=re.MULTILINE)

    # --- 2. Lists (Process *before* paragraphs) ---
    # 2a. Convert individual list items to <li> tags
    markdown_text = re.sub(r'^\* (.*)$', r'<li>\1</li>', markdown_text, flags=re.MULTILINE)
    markdown_text = re.sub(r'^[0-9]+\. (.*)$', r'<li>\1</li>', markdown_text, flags=re.MULTILINE)

    # 2b. Wrap consecutive <li> tags in <ul>
    markdown_text = re.sub(r'(<li>.*</li>(\n|$))+', r'<ul>\n\g<0>\n</ul>', markdown_text, flags=re.MULTILINE)

    # --- 3. Paragraphs (Process *after* lists) ---
    # Use negative lookahead and lookbehind to avoid wrapping already-tagged lines
    markdown_text = re.sub(r'^(?!<[a-z]>)([^#\n<>]+)(?<!</[a-z]>)$', r'<p>\1</p>', markdown_text, flags=re.MULTILINE)

    # --- 4. Bold and Italic --- (Can be done before or after paragraphs)
    markdown_text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', markdown_text)
    markdown_text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', markdown_text)

    # --- 5. Cleanup and Escaping ---
    markdown_text = re.sub(r'\s+', ' ', markdown_text).strip()  # Remove extra spaces
    markdown_text = re.sub(r'\n{2,}', '\n', markdown_text)      # Remove extra newlines

    # --- 6. IMPORTANT: HTML Entity Escaping (Do this *last*) ---
    markdown_text = markdown_text.replace('&', '&')
    markdown_text = markdown_text.replace('<', '<')
    markdown_text = markdown_text.replace('>', '>')
    markdown_text = markdown_text.replace('"', '"')
    markdown_text = markdown_text.replace("'", "'")

    return markdown_text
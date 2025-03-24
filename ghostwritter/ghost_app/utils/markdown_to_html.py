import markdown

def markdown_to_html(markdown_text):
    """
    Converts Markdown text to HTML using the 'markdown' library, suitable for WordPress.

    Args:
        markdown_text: The Markdown text to convert.

    Returns:
        The HTML generated from the Markdown text.
    """

    html = markdown.markdown(markdown_text, extensions=['extra', 'nl2br'])
    return html
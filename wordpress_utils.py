from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost

def create_wordpress_draft(title, content, wordpress_url, username, password):
    """Crée un brouillon d'article sur WordPress."""
    try:
        client = Client(wordpress_url, username, password)
        post = WordPressPost()
        post.title = title
        post.content = content
        post.post_status = 'draft'
        post_id = client.call(NewPost(post))
        return post_id
    except Exception as e:
        print(f"Erreur de publication sur wordpress : {e}")
        return None
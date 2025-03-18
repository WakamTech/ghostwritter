from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost

def create_wordpress_draft(title, content, wordpress_url, username, password):
    """Crée un brouillon d'article sur WordPress."""
    try:
        print("----- Inside create_wordpress_draft -----")  # DEBUG
        print(f"  - wordpress_url: {wordpress_url}")  # DEBUG
        print(f"  - username: {username}")  # DEBUG
        print(f"  - password: {password}")  # DEBUG
        print(f"  - title: {title}")  # DEBUG
        print(f"  - content: {content}")  # DEBUG

        client = Client(wordpress_url, username, password)
        print("----- Client created successfully -----")  # DEBUG

        post = WordPressPost()
        print("----- WordPressPost object created -----")  # DEBUG

        post.title = title
        print(f"----- Title set: {post.title} -----")  # DEBUG

        post.content = content
        print(f"----- Content set: {post.content} -----")  # DEBUG

        post.post_status = 'draft'
        print(f"----- Post status set: {post.post_status} -----")  # DEBUG

        print("----- Calling NewPost -----")  # DEBUG
        post_id = client.call(NewPost(post))  # This is where the error occurs
        print(f"----- Post ID: {post_id} -----")  # DEBUG
        return post_id

    except Exception as e:
        print(f"Erreur de publication sur wordpress : {e}")
        return None
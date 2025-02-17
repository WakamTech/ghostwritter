**Contenu du dossier :**

Dans le dossier que vous avez reçu, vous trouverez les éléments suivants :

1.  **L'exécutable :**
    *   `main.exe` : C'est le programme principal. C'est celui que vous devrez exécuter pour générer les articles.

2.  **Fichiers de configuration :**
    *   `prompt_article.txt` : Ce fichier contient les instructions pour la génération de l'article principal. Vous pouvez le modifier si vous souhaitez changer la manière dont les articles sont générés.
    *   `prompt_resume.txt` : Ce fichier contient les instructions pour la génération du résumé sous forme de tableau. Vous pouvez le modifier si vous souhaitez changer la manière dont les résumés sont générés.
    *   `requetes.csv` : Ce fichier contient les requêtes de recherche. Chaque requête doit être sur une nouvelle ligne. C'est ces requêtes qui seront utilisées pour générer les articles.
    *   `credentials_openai.csv` : Ce fichier contient les informations nécessaires pour accéder à l'API OpenAI. Il comprend votre clé API et le modèle de langue à utiliser. Assurez vous de bien le remplir.
    *   `credentials_wordpress.csv` : Ce fichier contient les informations nécessaires pour accéder à votre site WordPress. Il comprend l'URL de votre site, votre nom d'utilisateur et votre mot de passe. Assurez vous de bien le remplir.

**Étapes pour utiliser l'outil :**

1.  **Configuration des fichiers CSV et TXT :**
    *   **`credentials_openai.csv` :** Ouvrez ce fichier avec un éditeur de texte (Notepad, VS Code, etc.) ou un tableur (Excel, Google Sheets, etc.). Assurez-vous d'avoir une seule ligne de données en plus de l'entête.
        *   Renseignez votre clé API OpenAI à la place de `sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` dans la colonne `api_key`.
        *   Renseignez le modèle de langage que vous souhaitez utiliser (par exemple, `gpt-3.5-turbo`) dans la colonne `model`.
    *   **`credentials_wordpress.csv` :** Ouvrez ce fichier avec un éditeur de texte ou un tableur. Assurez-vous d'avoir une seule ligne de données en plus de l'entête.
        *   Renseignez l'URL de votre site WordPress avec le chemin vers le fichier `xmlrpc.php` (par exemple, `https://votresite.com/xmlrpc.php`) dans la colonne `wordpress_url`.
        *   Renseignez votre nom d'utilisateur WordPress dans la colonne `username`.
        *   Renseignez votre mot de passe WordPress dans la colonne `password`.
    *   **`requetes.csv` :** Ouvrez ce fichier avec un éditeur de texte ou un tableur.
        *   Inscrivez les requêtes sur lesquelles vous souhaitez générer des articles, une requête par ligne.
    *   **`prompt_article.txt` :** Vous pouvez modifier ce fichier si vous souhaitez modifier le prompt utilisé pour générer l'article.
    *    **`prompt_resume.txt` :** Vous pouvez modifier ce fichier si vous souhaitez modifier le prompt utilisé pour générer le résumé.
2.  **Exécution du programme :**
    *   Double-cliquez sur `main.exe`.
    *   Une fenêtre de terminal s'ouvrira et affichera la progression de l'outil.
    *   L'outil traitera chaque requête une par une, en respectant un délai de 5 minutes entre chaque requête pour éviter de surcharger l'API de Google.
    *   Une fois la génération des articles terminées, vous pourrez trouver vos brouillons sur votre WordPress.

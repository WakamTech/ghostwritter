# Gostwritter : Générateur Automatique d'Articles pour WordPress

Gostwritter est un script Python qui génère et publie automatiquement des articles sur plusieurs sites WordPress à partir de mots-clés fournis. Il utilise la recherche Google, les modèles GPT d'OpenAI et l'API XML-RPC de WordPress.

## Fonctionnalités

*   **Support Multi-Sites :** Gérez et publiez des articles sur plusieurs sites WordPress à partir d'une seule configuration.
*   **Génération Automatique de Contenu :** Génère des articles basés sur des mots-clés en utilisant les modèles GPT d'OpenAI.
*   **Intégration de la Recherche Google :** Utilise la recherche Google pour recueillir des informations pertinentes pour la génération d'articles.
*   **Publication Automatique sur WordPress :** Publie les articles en tant que brouillons sur vos sites WordPress.
*   **Saisie d'URL Simplifiée :** Les utilisateurs n'ont qu'à fournir l'URL de base de leurs sites WordPress (par exemple, `https://www.example.com`). Le script gère automatiquement le point de terminaison `/xmlrpc.php`.
*   **Exécutable Autonome :** Empaqueté en tant que fichier `.exe` unique pour une distribution et une utilisation faciles (Windows uniquement).
*   **Prompts Personnalisables :** Utilise des prompts configurables pour la génération d'articles et de résumés.

## Prérequis

*   **Python 3.7+ :** Assurez-vous d'avoir Python 3.7 ou une version supérieure installée.
*   **Clé API OpenAI :** Vous avez besoin d'une clé API OpenAI valide. Inscrivez-vous pour en obtenir une sur [https://platform.openai.com/](https://platform.openai.com/).
*   **Mot de Passe d'Application WordPress :** Pour chaque site WordPress, vous devez créer un *mot de passe d'application*.  **N'utilisez pas votre mot de passe WordPress principal.** Voir la section "Configuration de WordPress" ci-dessous.
*   **pip :** Le gestionnaire de paquets de Python. Il est généralement fourni avec Python.
* **requests** library: `pip install requests`
* **BeautifulSoup4** library: `pip install beautifulsoup4`
* **google-search-results** library: `pip install google-search-results`
* **openai**: `pip install openai`
* **python-wordpress-xmlrpc**: `pip install python-wordpress-xmlrpc`
* **PyInstaller**: `pip install pyinstaller`

## Installation et Configuration

1.  **Clonez le Répertoire (ou Téléchargez les Fichiers) :**



2.  **Installez les Dépendances :**



3.  **Créez les Fichiers de Configuration :**

    *   **`credentials_openai.csv` :**
        ```csv
        api_key,model
        votre_cle_api_openai,gpt-3.5-turbo-0125
        ```
        Remplacez `votre_cle_api_openai` par votre clé API OpenAI réelle. Vous pouvez changer le modèle si vous le souhaitez (et si vous y avez accès).

    *   **`credentials_wordpress.csv` :**
        ```csv
        username,password
        votre_nom_utilisateur_wordpress,votre_mot_de_passe_application
        ```
        Remplacez `votre_nom_utilisateur_wordpress` et `votre_mot_de_passe_application` par votre nom d'utilisateur WordPress et le *mot de passe d'application* (voir ci-dessous).

    *   **`sites_keywords.csv` :**
        ```csv
        site_url,keyword
        https://www.example.com,exemple mot-clé 1
        https://www.example.com,exemple mot-clé 2
        https://www.unautreexemple.com,un autre mot-clé 1
        ```
        Ajoutez une ligne pour chaque combinaison de site et de mot-clé. Utilisez l'*URL de base* de votre site WordPress (sans `/xmlrpc.php`).

    *   **`prompt_article.txt` :** Créez ce fichier et placez-y votre prompt pour la génération d'articles. Ce prompt sera utilisé avec OpenAI pour générer le contenu principal de l'article. Exemple :

        ```
        Vous êtes un assistant utile qui rédige des articles de blog informatifs et engageants. Rédigez un article complet sur le sujet suivant, en utilisant les informations fournies. L'article doit être bien structuré, avec des titres, des sous-titres et des puces lorsque cela est approprié. Visez une longueur d'environ 500 à 700 mots.  Sortie au format Markdown.
        ```

    *   **`prompt_resume.txt` :** Créez ce fichier pour votre prompt de génération de résumé. Exemple :
        ```
        Créez un résumé concis et informatif de l'article suivant, présenté sous forme de tableau HTML. Le tableau doit mettre en évidence les points clés et être facile à comprendre. Sortie en format Markdown.
        ```

4.  **Configuration de WordPress (Mot de Passe d'Application) :**

    *   Connectez-vous à votre tableau de bord WordPress.
    *   Accédez à votre profil utilisateur (généralement en cliquant sur votre photo de profil ou votre nom d'utilisateur).
    *   Recherchez la section "Mots de passe d'application" (l'emplacement exact peut varier en fonction de votre version de WordPress et de vos plugins).
    *   Créez un nouveau mot de passe d'application, donnez-lui un nom descriptif (par exemple, "Gostwritter"), et *copiez le mot de passe généré*. Vous ne le reverrez plus.
    *   Utilisez ce mot de passe d'application dans `credentials_wordpress.csv`.

    **Important :** Assurez-vous que XML-RPC est activé dans vos paramètres WordPress. Allez dans "Réglages" -> "Écriture" -> "Publication à distance" et cochez la case. Si vous utilisez un plugin de sécurité, il peut bloquer XML-RPC ; vous devrez peut-être mettre sur liste blanche l'adresse IP du script ou désactiver temporairement le plugin pendant la configuration.

## Utilisation
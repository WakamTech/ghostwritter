## Documentation Utilisateur – Dashboard de Configuration et Opérations

### Introduction

Ce dashboard est conçu pour configurer et exécuter des opérations de génération de contenu automatisée. Il est divisé en plusieurs sections principales, chacune gérant des aspects spécifiques de la configuration.

### Sections du Dashboard

1.  **Barre de Navigation**

    *   **Accès Rapide:** Utilisez la barre de navigation en haut de la page pour accéder rapidement aux différentes sections de configuration.
    *   **Liens:**
        *   Configuration Générale
        *   Sites et Mots-clés
        *   Prompts et Timing
        *   Opérations

2.  **Configuration Générale**

    *   **Paramètres Généraux:**
        *   Définissez les paramètres de base pour la génération de contenu.
        *   **Formulaire (`#general-config-form`):**
            *   Statut de publication des articles (brouillon, publié, etc.).
            *   Langue de recherche pour le contenu (fr, en, ...).
            *   Nombre de résultats de recherche à utiliser.
            *   Mode de génération (recherche, ou Direct.).
            *   Domaine de recherche préféré (.com, .fr, etc.).
            *   **Bouton "Enregistrer":** Enregistre les paramètres généraux.

        *   **Importation de Configuration:**
            *   **Bouton "Importer Configuration":** Permet d'importer un fichier de configuration au format JSON (`.json`).
            *   **Format du fichier JSON (exemple):**

                ```json
                {
                    "general_config": {
                        "post_status": "publish",
                        "search_language": "fr",
                        "num_results": 4,
                        "generation_mode": "search",
                        "search_domain": "com"
                    }
                }
                ```

    *   **Identifiants OpenAI:**
        *   Configurez les informations d'identification pour l'API OpenAI.
        *   **Formulaire (`#openai-config-form`):**
            *   `openai_api_key`: Votre clé API OpenAI.
            *   `openai_model`: Le modèle OpenAI à utiliser (par exemple, "gpt-4o").
        *    **Bouton "Enregistrer":** Enregistre la configuration API.
        *   **Importation (partie du fichier JSON):**
            ```json
             "openai_config": {
                "openai_api_key": "sk-votreCleAPI",
                "openai_model": "gpt-4o"
            }
            ```

    *   **Identifiants WordPress:**
        *   Configurez les informations de connexion pour votre site WordPress.
        *   **Formulaire (`#wordpress-config-form`):**
            *   `wordpress_username`: Nom d'utilisateur WordPress.
            *   `wordpress_password`: Mot de passe d'application WordPress.
       *    **Bouton "Enregistrer":** Enregistre la configuration API.
        *   **Importation (partie du fichier JSON):**

            ```json
            "wordpress_config": {
                "wordpress_username": "VotreNomUtilisateur",
                "wordpress_password": "VotreMotDePasseApplication"
            }
            ```

    * **Importation directe de l'ensemble :**
        * *   **Format du fichier JSON (exemple):**
        ```json
        {
            "general_config": {
                "post_status": "publish",
                "search_language": "fr",
                "num_results": 4,
                "generation_mode": "search",
                "search_domain": "com"
            },
            "openai_config": {
                "openai_api_key": "sk-votreCleAPI",
                "openai_model": "gpt-4o"
            },
            "wordpress_config": {
                "wordpress_username": "VotreNomUtilisateur",
                "wordpress_password": "VotreMotDePasseApplication"
            }
        }
        ```


3.  **Sites et Mots-clés (`#sites-keywords`)**

    *   **Tableau des Sites et Mots-clés:**
        *   Affiche une liste des sites (URLs) et des mots-clés associés.
        *   **Colonnes:**
            *   `URL Fournie`: L'URL du site.
            *   `Mot-clé`: Le mot-clé associé à l'URL.
            *   `Actions`:  Bouton "Supprimer" pour chaque ligne.
        *   **Bouton "Supprimer Tout":** Supprime tous les sites et mots-clés.  **Attention :** Cette action est irréversible.

    *   **Ajouter un Site et Mot-clé:**
        *   **Formulaire (`#add-site-keyword-form`):**
            *   `url`: Champ pour entrer l'URL du site.
            *   `keyword`: Champ pour entrer le mot-clé associé.
            *   **Bouton "Ajouter":** Ajoute la paire URL/mot-clé à la liste.

    *   **Importer des Sites et Mots-clés (CSV):**
        *   **Bouton "Importer CSV":** Permet d'importer une liste de sites et de mots-clés à partir d'un fichier CSV (`.csv`).
        *   **Format du fichier CSV:**

            ```
            url,keyword
            https://www.example.com,exemple mot-clé
            https://www.anotherexample.com,autre mot-clé
            ```
            *   Chaque ligne doit contenir l'URL et le mot-clé, séparés par une virgule.
            *  La première ligne doit être `url,keyword`

4.  **Prompts et Timing (`#prompts-timing`)**

    *   **Configuration des Prompts:**
        *   Définissez les instructions (prompts) à envoyer à l'API OpenAI.
        *   **Champs (dynamiques, dans `#timing-config-form`):**


    *   **Configuration du Timing:**
        *   Définissez les intervalles de temps entre les opérations.
        *   **Champs (dynamiques, dans `#timing-config-form`):**
        
        * **Bouton "Enregistrer Prompts et Timing":** Valide les modifications apportées aux prompts et aux temps d'attente.

5.  **Opérations (`#operations`)**

    *   **Lancer les Opérations:**
        *   **Bouton "Lancer les Opérations":** Démarre le processus de génération de contenu en utilisant la configuration actuelle.

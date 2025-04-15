from django import forms

class GeneralConfigForm(forms.Form):
    post_status = forms.ChoiceField(
        choices=[
            ('publish', 'Publié'),
            ('draft', 'Brouillon'),
            ('pending', 'En attente'),
            ('private', 'Privé'),
        ],
        label="Statut des articles",
        initial='publish' # Default value
    )
    search_language = forms.CharField(
        label="Langue de recherche",
        initial='fr' # Default value
    )
    num_results = forms.IntegerField(
        label="Nombre de résultats de recherche",
        initial=3, # Default value
        min_value=1 # Validation: minimum value
    )
    generation_mode = forms.ChoiceField(
        choices=[
            ('search', 'Recherche'),
            ('direct', 'Direct'),
        ],
        label="Mode de génération",
        initial='search' # Default value
    )
    search_domain = forms.CharField(
        label="Domaine de recherche",
        initial='com' # Default value
    )


class OpenAIConfigForm(forms.Form):
    openai_api_key = forms.CharField(
        label="API Key",
        widget=forms.Textarea(attrs={'rows': 2}) # Textarea widget for API key
    )
    openai_model = forms.CharField(
        label="Modèle",
        initial='gpt-4o' # Default value
    )


class WordPressConfigForm(forms.Form):
    wordpress_username = forms.CharField(label="Nom d'utilisateur")
    wordpress_password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput # PasswordInput widget for security
    )


class SiteKeywordForm(forms.Form):
    url = forms.CharField(
        label="URL du Site",
        widget=forms.URLInput(attrs={'placeholder': 'https://example.com'}) # URL input type and placeholder
    )
    keyword = forms.CharField(label="Mot-clé",  widget=forms.TextInput(attrs={'placeholder': 'Mot-clé principal'})) # Placeholder


class TimingConfigForm(forms.Form):
    # --- Champs Existant ---
    sleep_time = forms.IntegerField(
        label="Temps d'attente entre opérations (secondes)", # Label plus précis
        initial=3,
        min_value=0,
        help_text="Délai appliqué entre les appels API ou les mises à jour de sites pour éviter les surcharges."
    )
    prompt_article_v1_text = forms.CharField(
        label="Prompt Contenu Principal (Gutenberg/Classique)", # Renommé pour clarté vs ACF 'main_content'
        widget=forms.Textarea(attrs={'rows': 4}),
        required=False, # Rendre les prompts optionnels est souvent une bonne idée
        help_text="Prompt pour générer le contenu principal de l'éditeur WordPress standard."
    )
    prompt_article_v2_text = forms.CharField(
        label="Prompt Contenu Principal V2 (Optionnel)",
        widget=forms.Textarea(attrs={'rows': 4}),
        required=False,
        help_text="Variante du prompt pour le contenu principal, si nécessaire."
    )
    prompt_resume_text = forms.CharField(
        label="Prompt Résumé / Extrait",
        widget=forms.Textarea(attrs={'rows': 4}),
        required=False,
        help_text="Prompt pour générer l'extrait de l'article/page."
    )
    prompt_titre_text = forms.CharField(
        label="Prompt Titre (H1 / Titre de page WP)", # Potentiellement lié à ACF 'page_title'
        widget=forms.Textarea(attrs={'rows': 4}),
        required=False,
        help_text="Prompt pour générer le titre principal affiché sur la page."
    )
    prompt_meta_title_text = forms.CharField(
        label="Prompt Meta Title (SEO)",
        widget=forms.Textarea(attrs={'rows': 4}),
        required=False,
        help_text="Prompt pour générer la balise <title> à des fins SEO."
    )
    prompt_meta_description_text = forms.CharField( # Potentiellement lié à ACF 'meta_description'
        label="Prompt Meta Description (SEO)",
        widget=forms.Textarea(attrs={'rows': 4}),
        required=False,
        help_text="Prompt pour générer la meta description à des fins SEO."
    )

    # --- NOUVEAUX CHAMPS POUR PROMPTS ACF ---
    # On utilise la convention 'prompt_acf_<nom_champ>_text' pour les distinguer

    prompt_acf_main_content_text = forms.CharField(
        label="Prompt ACF: Contenu Principal (main_content)",
        widget=forms.Textarea(attrs={'rows': 4}),
        required=False,
        help_text="Prompt spécifique pour le champ ACF 'main_content'."
    )
    prompt_acf_vision_text = forms.CharField(
        label="Prompt ACF: Vision (vision)",
        widget=forms.Textarea(attrs={'rows': 4}),
        required=False,
        help_text="Prompt spécifique pour le champ ACF 'vision'."
    )
    prompt_acf_faqs_text = forms.CharField( # Pour la section FAQ principale si différente des numérotées
        label="Prompt ACF: FAQs (faqs - section)",
        widget=forms.Textarea(attrs={'rows': 4}),
        required=False,
        help_text="Prompt pour la section principale des FAQs (si 'faqs' est un champ global)."
    )
    # Note: meta_description ACF est peut-être déjà couvert par prompt_meta_description_text ? À clarifier.
    # Si le champ ACF 'meta_description' DOIT être différent du Meta Desc SEO, ajoutez :
    # prompt_acf_meta_description_text = forms.CharField(...)

    prompt_acf_promotion_text = forms.CharField(
        label="Prompt ACF: Promotion (promotion)",
        widget=forms.Textarea(attrs={'rows': 4}),
        required=False,
        help_text="Prompt spécifique pour le champ ACF 'promotion'."
    )
    prompt_acf_slots_description_text = forms.CharField(
        label="Prompt ACF: Description Slots (slots_description)",
        widget=forms.Textarea(attrs={'rows': 4}),
        required=False,
        help_text="Prompt spécifique pour le champ ACF 'slots_description'."
    )
    prompt_acf_short_description_text = forms.CharField(
        label="Prompt ACF: Description Courte (short_description)",
        widget=forms.Textarea(attrs={'rows': 4}),
        required=False,
        help_text="Prompt spécifique pour le champ ACF 'short_description'."
    )
    # Note: page_title ACF est peut-être déjà couvert par prompt_titre_text ? À clarifier.
    # Si le champ ACF 'page_title' DOIT être différent du Titre WP, ajoutez :
    # prompt_acf_page_title_text = forms.CharField(...)

    prompt_acf_introduction_text = forms.CharField(
        label="Prompt ACF: Introduction (introduction)",
        widget=forms.Textarea(attrs={'rows': 4}),
        required=False,
        help_text="Prompt spécifique pour le champ ACF 'introduction'."
    )
    prompt_acf_playing_with_crypto_text = forms.CharField(
        label="Prompt ACF: Jouer avec Crypto (playing_with_crypto)",
        widget=forms.Textarea(attrs={'rows': 4}),
        required=False,
        help_text="Prompt spécifique pour le champ ACF 'playing_with_crypto'."
    )
    prompt_acf_contact_details_text = forms.CharField(
        label="Prompt ACF: Détails Contact (contact_details)",
        widget=forms.Textarea(attrs={'rows': 4}),
        required=False,
        help_text="Prompt spécifique pour le champ ACF 'contact_details' (si pertinent pour génération)."
    )

    # --- Champs ACF Répétitifs (FAQs, Glossaire, News) ---
    # Utiliser des tailles de textarea plus petites (rows=2) peut être judicieux
    prompt_acf_faqs_1_text = forms.CharField(label="Prompt ACF: FAQ 1", widget=forms.Textarea(attrs={'rows': 2}), required=False)
    prompt_acf_faqs_2_text = forms.CharField(label="Prompt ACF: FAQ 2", widget=forms.Textarea(attrs={'rows': 2}), required=False)
    prompt_acf_faqs_3_text = forms.CharField(label="Prompt ACF: FAQ 3", widget=forms.Textarea(attrs={'rows': 2}), required=False)
    prompt_acf_faqs_4_text = forms.CharField(label="Prompt ACF: FAQ 4", widget=forms.Textarea(attrs={'rows': 2}), required=False)
    prompt_acf_faqs_5_text = forms.CharField(label="Prompt ACF: FAQ 5", widget=forms.Textarea(attrs={'rows': 2}), required=False)
    prompt_acf_faqs_6_text = forms.CharField(label="Prompt ACF: FAQ 6", widget=forms.Textarea(attrs={'rows': 2}), required=False)

    prompt_acf_glossary_1_text = forms.CharField(label="Prompt ACF: Glossaire 1", widget=forms.Textarea(attrs={'rows': 2}), required=False)
    prompt_acf_glossary_2_text = forms.CharField(label="Prompt ACF: Glossaire 2", widget=forms.Textarea(attrs={'rows': 2}), required=False)
    prompt_acf_glossary_3_text = forms.CharField(label="Prompt ACF: Glossaire 3", widget=forms.Textarea(attrs={'rows': 2}), required=False)
    prompt_acf_glossary_test_text = forms.CharField(label="Prompt ACF: Glossaire Test", widget=forms.Textarea(attrs={'rows': 2}), required=False) # Gardé comme demandé

    prompt_acf_news_1_text = forms.CharField(label="Prompt ACF: News 1", widget=forms.Textarea(attrs={'rows': 2}), required=False)
    prompt_acf_news_2_text = forms.CharField(label="Prompt ACF: News 2", widget=forms.Textarea(attrs={'rows': 2}), required=False)
    prompt_acf_news_3_text = forms.CharField(label="Prompt ACF: News 3", widget=forms.Textarea(attrs={'rows': 2}), required=False)

    prompt_acf_terms_text = forms.CharField(
        label="Prompt ACF: Termes (terms)",
        widget=forms.Textarea(attrs={'rows': 4}),
        required=False,
        help_text="Prompt spécifique pour le champ ACF 'terms'."
    )

    # Optionnel: Ajouter une méthode clean pour valider des relations entre champs si nécessaire
    # def clean(self):
    #     cleaned_data = super().clean()
    #     # ... vos validations ...
    #     return cleaned_data

    # Optionnel: Rendre l'affichage plus dynamique si besoin (pas nécessaire avec le template actuel)
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     # Modifier dynamiquement les widgets ou labels si besoin ici
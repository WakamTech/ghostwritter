from django.shortcuts import render
from .forms import GeneralConfigForm, OpenAIConfigForm, WordPressConfigForm, SiteKeywordForm, TimingConfigForm 
from .utils import config_utils  # Import the config_utils module, 
import json # Import the json module
import csv
import time
from .utils import google_search, content_extractor, openai_utils, wordpress_utils, markdown_to_html
from urllib.parse import urljoin, urlparse

POSSIBLE_ACF_MESSAGES_KEYS = [
    'main_content', 'vision', 'faqs', 'meta_description', 'promotion',
    'slots_description', 'short_description', 'page_title', 'introduction',
    'playing_with_crypto', 'contact_details', 'faqs_1', 'faqs_2', 'faqs_3',
    'faqs_4', 'faqs_5', 'faqs_6', 'glossary_1', 'glossary_2', 'glossary_3',
    'glossary_test', 'news_1', 'news_2', 'news_3', 'terms', 'meta_title' # meta_title ajouté ici aussi
]

def dashboard_view(request):
    # Load initial configurations from JSON files
    initial_general_config = config_utils.load_general_config()
    initial_openai_config = config_utils.load_openai_config()
    initial_wordpress_config = config_utils.load_wordpress_config()
    initial_timing_config = config_utils.load_timing_config() # Load timing config
    timing_form = TimingConfigForm(initial=initial_timing_config) # Create TimingConfigForm instance with initial data

    general_form = GeneralConfigForm(initial=initial_general_config) # Initialize forms with loaded data
    openai_form = OpenAIConfigForm(initial=initial_openai_config)
    wordpress_form = WordPressConfigForm(initial=initial_wordpress_config)
    
    # --- Load sites_keywords data using config_utils ---
    sites_keywords_data = config_utils.load_sites_keywords() # Load using the new function
    
    site_keyword_form = SiteKeywordForm() # Create an instance of SiteKeywordForm

    if request.method == 'POST':
        
        if 'save_general_config' in request.POST:
            general_form = GeneralConfigForm(request.POST)
            if general_form.is_valid():
                general_config_data = general_form.cleaned_data
                config_utils.save_general_config(general_config_data) # Save to JSON file
                print("--- General Configuration Data Saved to JSON ---")
                general_form = GeneralConfigForm(initial=general_config_data) # Re-populate

        elif 'save_openai_config' in request.POST:
            openai_form = OpenAIConfigForm(request.POST)
            if openai_form.is_valid():
                openai_config_data = openai_form.cleaned_data
                config_utils.save_openai_config(openai_config_data) # Save to JSON file
                print("--- OpenAI Configuration Data Saved to JSON ---")
                openai_form = OpenAIConfigForm(initial=openai_config_data)

        elif 'save_wordpress_config' in request.POST:
            wordpress_form = WordPressConfigForm(request.POST)
            if wordpress_form.is_valid():
                wordpress_config_data = wordpress_form.cleaned_data
                config_utils.save_wordpress_config(wordpress_config_data) # Save to JSON file
                print("--- WordPress Configuration Data Saved to JSON ---")
                wordpress_form = WordPressConfigForm(initial=wordpress_config_data)
                
        elif 'config_file' in request.FILES: # Check if a file was uploaded (name from input)
            print("okj,nbgvfcds")
            config_file = request.FILES['config_file'] # Get the uploaded file
            try:
                config_data = json.load(config_file) # Load JSON data from the file
                print("--- Configuration File Imported ---")
                print(config_data)

                # --- Apply imported configurations ---
                if 'general_config' in config_data:
                    config_utils.save_general_config(config_data['general_config'])
                    initial_general_config = config_data['general_config'] # Update initial config for re-populating
                    general_form = GeneralConfigForm(initial=initial_general_config) # Re-populate form

                if 'openai_config' in config_data:
                    config_utils.save_openai_config(config_data['openai_config'])
                    initial_openai_config = config_data['openai_config']
                    openai_form = OpenAIConfigForm(initial=initial_openai_config)

                if 'wordpress_config' in config_data:
                    config_utils.save_wordpress_config(config_data['wordpress_config'])
                    initial_wordpress_config = config_data['wordpress_config']
                    wordpress_form = WordPressConfigForm(initial=initial_wordpress_config)

                print("--- Configurations Loaded from File ---")

            except json.JSONDecodeError:
                print("--- Error: Invalid JSON file uploaded ---")
                # Optionally, add form error handling to display an error message in the template

        elif 'add_site_keyword' in request.POST:
            site_keyword_form = SiteKeywordForm(request.POST)
            if site_keyword_form.is_valid():
                new_site_keyword_data = site_keyword_form.cleaned_data
                print("--- Adding new Site and Keyword ---")
                print(new_site_keyword_data)

                # --- Append to sites_keywords.csv and reload using config_utils ---
                sites_keywords_data = config_utils.load_sites_keywords() # Load current data
                sites_keywords_data.append(new_site_keyword_data) # Append new data
                config_utils.save_sites_keywords(sites_keywords_data) # Save the updated list
                print(f"--- Successfully added and saved to sites_keywords.csv ---")


                site_keyword_form = SiteKeywordForm() # Clear the form


        elif 'delete_site_keyword' in request.POST: # Check for "delete_site_keyword" button click
            url_to_delete = request.POST.get('delete_url') # Get the URL from the hidden input
            if url_to_delete:
                print(f"--- Deleting Site/Keyword with URL: {url_to_delete} ---")

                sites_keywords_data = config_utils.load_sites_keywords() # Load current data
                updated_sites_keywords_data = [
                    item for item in sites_keywords_data if item['url'] != url_to_delete # Filter out the item to delete
                ]
                config_utils.save_sites_keywords(updated_sites_keywords_data) # Save the updated list
                sites_keywords_data = updated_sites_keywords_data # Update sites_keywords_data in the view

                print(f"--- Successfully deleted and saved to sites_keywords.csv ---")

        elif 'delete_all_sites_keywords' in request.POST: # Check for "Supprimer Tout" button
            print("--- Deleting ALL Sites and Keywords ---")

            config_utils.save_sites_keywords([]) # Save an empty list to clear sites_keywords.csv
            sites_keywords_data = [] # Clear sites_keywords_data in the view

            print("--- Successfully deleted ALL sites and keywords from sites_keywords.csv ---")


        elif 'sites_keywords_csv_file' in request.FILES: # Check for CSV file upload
            print("Entering 'sites_keywords_csv_file' block in views.py") # ADD THIS LINE
            print("request.FILES:", request.FILES) # ADD THIS LINE
            csv_file = request.FILES['sites_keywords_csv_file'] # Get the uploaded file

            if not csv_file.name.endswith('.csv'): # Basic file type validation
                print("--- Error: Uploaded file is not a CSV ---")
                #  Ideally, add error message to template here
            else:
                try:
                    decoded_file = csv_file.read().decode('utf-8') # Decode file content
                    csv_data = csv.DictReader(decoded_file.splitlines()) # Read CSV data using DictReader
                    imported_sites_keywords = list(csv_data) # Convert CSV reader to a list of dictionaries
                    print("--- CSV File Imported ---")
                    print(f"Imported {len(imported_sites_keywords)} entries from CSV")

                    current_sites_keywords_data = config_utils.load_sites_keywords() # Load existing data
                    updated_sites_keywords_data = current_sites_keywords_data + imported_sites_keywords # Append imported data

                    config_utils.save_sites_keywords(updated_sites_keywords_data) # Save combined data
                    sites_keywords_data = updated_sites_keywords_data # Update for template

                    print("--- Successfully imported and saved CSV data to sites_keywords.csv ---")

                except Exception as e:
                    print(f"--- Error processing CSV file: {e} ---")
                    #  Ideally, add error message to template here

        elif 'save_timing_config' in request.POST:
            print('timing')
            # print(request.data)
            timing_form = TimingConfigForm(request.POST)
            if timing_form.is_valid():
                timing_config_data = timing_form.cleaned_data
                config_utils.save_timing_config(timing_config_data) # Save timing config (now includes prompt texts)
                print("--- Timing Configuration Data Saved to JSON (including prompt paths) ---")
                timing_form = TimingConfigForm(initial=timing_config_data) # Re-populate form

        elif 'start_operations' in request.POST: # Check for "Lancer les Opérations" button
            print("--- Operations Started! ---")
            run_operations() # Call the function to execute operations
            print("--- Operations Completed (Simulated) ---")


    context = {
        'general_form': general_form,
        'openai_form': openai_form,
        'wordpress_form': wordpress_form,
        'sites_keywords': sites_keywords_data,
        'site_keyword_form': site_keyword_form,
        'timing_form': timing_form, 
    }
    return render(request, 'ghost_app/index.html', context)

def run_operations():
    print("--- Running Operations ---")

    # --- Load Configurations ---
    general_config = config_utils.load_general_config()
    openai_config = config_utils.load_openai_config()
    wordpress_config = config_utils.load_wordpress_config()
    timing_config = config_utils.load_timing_config() # Contient tous les prompts
    sites_keywords_data = config_utils.load_sites_keywords()

    # --- Extract Configurations ---
    openai_api_key = openai_config.get('openai_api_key', '')
    openai_model = openai_config.get('openai_model', 'gpt-3.5-turbo')
    wordpress_username = wordpress_config.get('wordpress_username', '')
    wordpress_password = wordpress_config.get('wordpress_password', '')
    post_status = general_config.get('post_status', 'publish') # Publier par défaut peut-être?
    search_language = general_config.get('search_language', 'fr')
    search_domain = general_config.get('search_domain', 'com')
    num_results = general_config.get('num_results', 3)
    generation_mode = general_config.get('generation_mode', 'search')
    sleep_time = timing_config.get('sleep_time', 3)

    # --- Load ALL necessary prompts from timing_config ---
    prompts = {}
    # Charger les prompts spécifiques v1/v2
    prompts['v1'] = timing_config.get('prompt_article_v1_text', '')
    prompts['v2'] = timing_config.get('prompt_article_v2_text', '')
    prompts['summary'] = timing_config.get('prompt_resume_text', '') # Pour le résumé/tableau
    prompts['main_title'] = timing_config.get('prompt_titre_text', '') # Titre principal WP/Page

    # Charger les prompts pour les clés ACF
    for key in POSSIBLE_ACF_MESSAGES_KEYS:
        prompt_config_key = f'prompt_{key}_text' # Ex: prompt_meta_title_text
        prompts[key] = timing_config.get(prompt_config_key, '')
        if not prompts[key]:
            print(f"--- WARNING: Prompt for ACF key '{key}' (config key '{prompt_config_key}') is missing or empty! ---")


    # --- Process each site and keyword ---
    for site_keyword_item in sites_keywords_data:
        provided_url = site_keyword_item.get('url')
        query = site_keyword_item.get('keyword') # Le mot clé pour la génération

        if not provided_url or not query:
            print(f"--- Skipping entry: Missing URL or keyword: {site_keyword_item} ---")
            continue

        print(f"\n--- Processing URL: {provided_url}, Keyword: {query} ---")

        try:
            # --- 1. Determine WordPress URL, ID, and Type ---
            parsed_url = urlparse(provided_url)
            base_wordpress_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
            full_wordpress_url = base_wordpress_url # Utiliser la base pour l'API
            slug = parsed_url.path.strip('/') if parsed_url.path and parsed_url.path != '/' else None

            post_id = None
            post_type = 'page' # Default to page

            if not slug: # Home page?
                print("--- URL seems to be Home Page, checking settings... ---")
                post_id = wordpress_utils.get_home_page_id(full_wordpress_url, wordpress_username, wordpress_password)
                if post_id:
                    post_type = 'page' # Home page is always a page
                    print(f"--- Home Page ID found: {post_id}, Type: {post_type} ---")
                else:
                    print("--- ERROR: Could not retrieve Home Page ID or it's not a static page. Skipping this URL. ---")
                    continue
            else: # Not home page, try to find by slug
                print(f"--- Trying to find existing content by slug: '{slug}' ---")
                post_id, found_type = wordpress_utils.get_post_id_from_slug(full_wordpress_url, wordpress_username, wordpress_password, slug, post_type='page') # Prioritize page
                if post_id:
                    post_type = found_type # Use the type it was found as ('page' or 'post')
                    print(f"--- Existing content found. ID: {post_id}, Type: {post_type} ---")
                else:
                    print(f"--- No existing content found for slug '{slug}'. Will create a new '{post_type}'. ---")
                    post_id = None # Ensure post_id is None for creation path


            # --- 2. Prepare Data Payload ---
            wp_data_payload = {
                'status': post_status,
                # 'title': ?, # Sera défini ci-dessous
                # 'content': ?, # Champ WP standard, optionnel si tout est dans ACF
                # 'acf_messages': ? # Sera défini ci-dessous
            }

            # --- 3. Generate Base Content (Main Article) ---
            # This content is used as context for generating all other fields
            print(f"--- Generating base article content (Mode: {generation_mode}) ---")
            base_article_content_md = "" # Markdown content
            if generation_mode == 'search':
                prompt_to_use = prompts.get('v1')
                if not prompt_to_use:
                     print("--- ERROR: Prompt V1 is missing! Cannot generate content. Skipping. ---")
                     continue
                search_urls = google_search.get_organic_urls(query, num_results=int(num_results), lang=search_language, tld=search_domain)
                if search_urls:
                    print(f"--- Found {len(search_urls)} URLs from search. Extracting text... ---")
                    all_text_content = "".join([content_extractor.extract_text_from_url(url) or "" for url in search_urls])
                    if not all_text_content.strip():
                         print(f"--- WARNING: Extracted text from search results is empty for query '{query}'. Cannot generate reliable content. Skipping. ---")
                         continue
                    base_article_content_md = openai_utils.generate_article(prompt_to_use, all_text_content, openai_api_key, query, openai_model)
                else:
                    print(f"--- No search results found for query: '{query}'. Cannot generate content in 'search' mode. Skipping. ---")
                    continue # Skip this item if no search results in search mode
            elif generation_mode == 'direct':
                prompt_to_use = prompts.get('v2')
                if not prompt_to_use:
                     print("--- ERROR: Prompt V2 is missing! Cannot generate content. Skipping. ---")
                     continue
                base_article_content_md = openai_utils.generate_article(prompt_to_use, "", openai_api_key, query, openai_model)

            if not base_article_content_md:
                print(f"--- ERROR: Failed to generate base article content for query: '{query}'. Skipping. ---")
                continue

            print("--- Base article content generated (Markdown) ---")
            # print(base_article_content_md[:200] + "...") # Print snippet

            # --- 4. Generate WP Title ---
            print("--- Generating WordPress Page Title ---")
            wp_title_prompt = prompts.get('main_title')
            if not wp_title_prompt:
                 print("--- WARNING: Prompt for main title ('prompt_titre_text') is missing. Using keyword as title. ---")
                 wp_data_payload['title'] = query.capitalize() # Fallback title
            else:
                 generated_title = openai_utils.generate_title(wp_title_prompt, base_article_content_md, openai_api_key, openai_model)
                 wp_data_payload['title'] = generated_title.strip('"«»‘’“” ') # Clean up quotes/spaces

            print(f"--- Generated WP Title: {wp_data_payload['title']} ---")


            # --- 5. Handle ACF Messages (Create vs Update) ---
            new_acf_messages = []

            if post_id:
                # --- UPDATE PATH ---
                print(f"--- UPDATE PATH for Post ID: {post_id} ---")
                print("--- Fetching existing page data... ---")
                existing_data = wordpress_utils.get_post_data(post_id, full_wordpress_url, wordpress_username, wordpress_password, post_type)

                if not existing_data:
                    print(f"--- ERROR: Failed to fetch existing data for ID {post_id}. Cannot update. Skipping. ---")
                    continue

                existing_acf_messages = existing_data.get('acf_messages', [])
                if not isinstance(existing_acf_messages, list): # Sanity check
                     print(f"--- WARNING: Existing 'acf_messages' is not a list for ID {post_id}. Treating as empty. Data: {existing_acf_messages}")
                     existing_acf_messages = []

                print(f"--- Found {len(existing_acf_messages)} existing ACF message rows. Processing relevant keys... ---")

                # Get list of meta_keys present in the existing page's acf_messages
                keys_to_regenerate = {msg.get('meta_key') for msg in existing_acf_messages if msg.get('meta_key') in POSSIBLE_ACF_MESSAGES_KEYS}
                print(f"--- Meta keys found in existing ACF to regenerate: {keys_to_regenerate} ---")


                # Regenerate content for each required key
                for meta_key in keys_to_regenerate:
                    prompt_text = prompts.get(meta_key)
                    if not prompt_text:
                        print(f"--- WARNING: No prompt found for meta_key '{meta_key}'. Cannot generate content for this field. Skipping ACF row. ---")
                        continue

                    print(f"--- Generating content for ACF meta_key: '{meta_key}' ---")
                    generated_content = ""
                    try:
                        if meta_key == 'main_content':
                            # Special handling: combine summary and main article
                            summary_prompt = prompts.get('summary')
                            if summary_prompt:
                                print("--- Generating summary for main_content ---")
                                article_summary = openai_utils.generate_summary_table(summary_prompt, base_article_content_md, openai_api_key, openai_model)
                            else:
                                print("--- WARNING: Summary prompt missing. Skipping summary. ---")
                                article_summary = ""

                            # Convert main markdown to HTML
                            article_html_content = markdown_to_html.markdown_to_html(base_article_content_md)
                            # Combine summary (if exists) and main content HTML
                            generated_content = f"{article_summary}\n{article_html_content}".strip()
                            # Optionally update the main WP content field as well?
                            # wp_data_payload['content'] = generated_content

                        elif meta_key == 'meta_title' or meta_key == 'page_title': # Use generate_title for titles
                             generated_content = openai_utils.generate_title(prompt_text, base_article_content_md, openai_api_key, openai_model).strip('"«»‘’“” ')
                        elif meta_key == 'meta_description' or meta_key == 'short_description' or meta_key == 'introduction': # Use generate_summary for descriptions/intros
                             generated_content = openai_utils.generate_summary(prompt_text, base_article_content_md, openai_api_key, openai_model) # Need generate_summary
                        else: # Use a generic generation for other fields (like vision, faqs, etc.)
                            # Assuming generate_article can work as a generic generator here
                            # Or create openai_utils.generate_generic(prompt, context, ...)
                             generated_content = openai_utils.generate_article(prompt_text, base_article_content_md, openai_api_key, query, openai_model) # Pass query for context too?

                        if generated_content:
                            print(f"--- Generated content for '{meta_key}' (snippet): {generated_content[:100]}... ---")
                            # Add to the new acf_messages list
                            new_acf_messages.append({
                                "role": "user", # Keep structure similar to example
                                "gpt": True,
                                "content": prompt_text, # Store the *prompt* used in 'content'? Or the generated result? Your example has prompt here. Let's keep prompt.
                                "result": generated_content, # Store the *result* here
                                "meta_key": meta_key,
                                "status": "completed", # Mark as completed
                                "completed_date": time.strftime("%Y-%m-%d %H:%M:%S")
                            })
                        else:
                            print(f"--- WARNING: Failed to generate content for meta_key '{meta_key}'. Skipping ACF row. ---")

                    except Exception as gen_e:
                        print(f"--- ERROR during OpenAI generation for meta_key '{meta_key}': {gen_e}. Skipping ACF row. ---")


            else:
                # --- CREATE PATH ---
                print(f"--- CREATE PATH for new page ---")
                # Define the default ACF messages to create
                default_keys_to_create = ['main_content', 'meta_title', 'meta_description']
                print(f"--- Will create default ACF message rows for: {default_keys_to_create} ---")

                for meta_key in default_keys_to_create:
                    prompt_text = prompts.get(meta_key)
                    if not prompt_text:
                        if meta_key != 'main_content' :
                            print(f"--- WARNING: No prompt found for default meta_key '{meta_key}'. Cannot generate content. Skipping ACF row. ---")
                            continue

                    print(f"--- Generating content for default ACF meta_key: '{meta_key}' ---")
                    generated_content = ""
                    try:
                        if meta_key == 'main_content':
                            summary_prompt = prompts.get('summary')
                            if summary_prompt:
                                print("--- Generating summary for main_content ---")
                                article_summary = openai_utils.generate_summary_table(summary_prompt, base_article_content_md, openai_api_key, openai_model)
                            else:
                                article_summary = ""
                            article_html_content = markdown_to_html.markdown_to_html(base_article_content_md)
                            generated_content = f"{article_summary}\n{article_html_content}".strip()
                            # Optionally set the main WP content field on creation?
                            # wp_data_payload['content'] = generated_content
                        elif meta_key == 'meta_title':
                            generated_content = openai_utils.generate_title(prompt_text, base_article_content_md, openai_api_key, openai_model).strip('"«»‘’“” ')
                        elif meta_key == 'meta_description':
                            generated_content = openai_utils.generate_title(prompt_text, base_article_content_md, openai_api_key, openai_model) # Need generate_summary

                        if generated_content:
                            print(f"--- Generated content for '{meta_key}' (snippet): {generated_content[:100]}... ---")
                            new_acf_messages.append({
                                "role": "user",
                                "gpt": True,
                                "content": prompt_text, # Store prompt
                                "result": generated_content, # Store result
                                "meta_key": meta_key,
                                "status": "completed", # Mark as completed
                                "completed_date": time.strftime("%Y-%m-%d %H:%M:%S")
                            })
                        else:
                             print(f"--- WARNING: Failed to generate content for default meta_key '{meta_key}'. Skipping ACF row. ---")
                    except Exception as gen_e:
                        print(f"--- ERROR during OpenAI generation for default meta_key '{meta_key}': {gen_e}. Skipping ACF row. ---")

            # --- Add the generated ACF messages to the payload ---
            if new_acf_messages:
                 wp_data_payload['acf_messages'] = new_acf_messages
            else:
                 print("--- WARNING: No ACF messages were generated or added to the payload. ---")
                 # Decide if you want to send an empty list or omit the key
                 # wp_data_payload['acf_messages'] = []


            # --- 6. Execute Create or Update ---
            print(f"--- Preparing to {'UPDATE' if post_id else 'CREATE'} resource ---")
            # Note: Pass post_type determined earlier (page or post)
            result = wordpress_utils.create_or_update_wordpress_resource(
                wp_data_payload,
                full_wordpress_url,
                wordpress_username,
                wordpress_password,
                post_id=post_id,
                post_type=post_type
            )

            if post_id: # Update
                if result: # result is True on successful update
                    print(f"--- SUCCESS: Page/Post updated successfully on {full_wordpress_url} (ID: {post_id}) ---")
                else:
                    print(f"--- FAILURE: Failed to update Page/Post on {full_wordpress_url} (ID: {post_id}) ---")
            else: # Create
                if result: # result is the new ID on successful creation
                    print(f"--- SUCCESS: Page/Post created successfully with ID: {result} on {full_wordpress_url} ---")
                else:
                    print(f"--- FAILURE: Failed to create Page/Post on {full_wordpress_url} ---")


            # --- 7. Sleep ---
            print(f"--- Sleeping for {sleep_time} seconds ---")
            time.sleep(int(sleep_time))

        except Exception as e:
            print(f"--- 💥 UNHANDLED ERROR processing URL: {provided_url}, Keyword: {query} ---")
            import traceback
            traceback.print_exc() # Print full traceback for debugging
            print("--- Moving to the next entry... ---")
            continue # Move to the next item in the loop

    print("--- End of All Operations ---")
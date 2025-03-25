from django.shortcuts import render
from .forms import GeneralConfigForm, OpenAIConfigForm, WordPressConfigForm, SiteKeywordForm, TimingConfigForm 
from .utils import config_utils  # Import the config_utils module, 
import json # Import the json module
import csv
import time
from .utils import google_search, content_extractor, openai_utils, wordpress_utils, markdown_to_html
from urllib.parse import urljoin, urlparse

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

# In your views.py

def run_operations():
    print("--- Running Operations ---")

    # --- Load Configurations ---
    general_config = config_utils.load_general_config()
    openai_config = config_utils.load_openai_config()
    wordpress_config = config_utils.load_wordpress_config()
    timing_config = config_utils.load_timing_config()
    sites_keywords_data = config_utils.load_sites_keywords()

    # --- Extract Configurations ---
    openai_api_key = openai_config.get('openai_api_key', '')
    openai_model = openai_config.get('openai_model', 'gpt-3.5-turbo') # Default model
    wordpress_username = wordpress_config.get('wordpress_username', '')
    wordpress_password = wordpress_config.get('wordpress_password', '')
    post_status = general_config.get('post_status', 'draft') # Default to draft
    search_language = general_config.get('search_language', 'fr') # Default to French
    search_domain = general_config.get('search_domain', 'com') # Default to .com
    num_results = general_config.get('num_results', 3) # Default to 3
    generation_mode = general_config.get('generation_mode', 'search') # Default to 'search'
    sleep_time = timing_config.get('sleep_time', 3) # Default sleep time
    prompt_article_v1 = timing_config.get('prompt_article_v1_text', '') # Get prompt texts
    prompt_article_v2 = timing_config.get('prompt_article_v2_text', '')
    prompt_resume = timing_config.get('prompt_resume_text', '')
    prompt_titre_prompt = timing_config.get('prompt_titre_text', '') # Renamed variable


    # --- Process each site and keyword ---
    for site_keyword_item in sites_keywords_data:
        provided_url = site_keyword_item.get('url')
        query = site_keyword_item.get('keyword')

        if not provided_url or not query:
            print(f"--- Skipping entry: Missing URL or keyword in sites_keywords data ---")
            continue

        print(f"\n--- Processing URL: {provided_url}, Keyword: {query} ---")

        try:
            # --- 1. Determine WordPress URL and Post ID ---
            parsed_url = urlparse(provided_url)
            base_wordpress_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
            full_wordpress_url = base_wordpress_url  # Use base URL for REST API
            slug = parsed_url.path.strip('/') if parsed_url.path and parsed_url.path != '/' else None

            post_id = None
            post_type = 'post'  # Default, will be overridden for home page


            if not slug:  # It's likely the home page
                print("--- Detecting Home Page URL ---")
                post_id = wordpress_utils.get_home_page_id(full_wordpress_url, wordpress_username, wordpress_password)
                if post_id:
                    post_type = 'page'  # Home page is *always* a page
                    print(f"--- Home Page ID found: {post_id} ---")
                else:
                    print("--- ERROR: Could not retrieve Home Page ID. Skipping this URL. ---")
                    continue  # Skip if home page ID can't be found
            elif slug: # If a slug is extracted from the URL, try to get existing post/page
                post_id = wordpress_utils.get_post_id_from_slug(full_wordpress_url, wordpress_username, wordpress_password, slug, post_type='page')
                if post_id:
                    post_type = 'page'
                else:
                    post_id = wordpress_utils.get_post_id_from_slug(full_wordpress_url, wordpress_username, wordpress_password, slug, post_type='post')
                    if not post_id:
                        print(f"No existing post or page found for slug '{slug}'. Creating new post.")

            # --- 2. Generate Article Content (Rest of the logic remains the same) ---
            article_content = ""
            if generation_mode == 'search':
                search_urls = google_search.get_organic_urls(query, num_results=int(num_results), lang=search_language, tld=search_domain)
                if search_urls:
                    all_text_content = "".join([content_extractor.extract_text_from_url(url) or "" for url in search_urls])
                    article_content = openai_utils.generate_article(prompt_article_v1, all_text_content, openai_api_key, query, openai_model)
                else:
                    print(f"No search results found for query: {query}")
                    continue

            elif generation_mode == 'direct':
                article_content = openai_utils.generate_article(prompt_article_v2, "", openai_api_key, query, openai_model)

            if not article_content:
                print(f"Failed to generate article content for: {query}")
                continue

            # --- 3. Generate Title and Summary ---
            article_title = openai_utils.generate_title(prompt_titre_prompt, article_content, openai_api_key, openai_model).strip('"').strip('«').strip('»')
            article_summary = openai_utils.generate_summary_table(prompt_resume, article_content, openai_api_key, openai_model)

            if not article_title or not article_summary:
                print(f"Failed to generate title or summary for: {query}")
                continue

            # --- 4. Convert Markdown to HTML and Combine Content ---
            article_html_content = markdown_to_html.markdown_to_html(article_content)
            full_post_content = f"<p>{article_summary}</p><p>{article_html_content}</p>"

            # --- 5. Create or Update WordPress Post/Page ---
            # The key change is that if post_id exists (either from slug or home page), it *always* updates.
            post_result = wordpress_utils.create_or_update_wordpress_post(
                article_title, full_post_content, full_wordpress_url, wordpress_username, wordpress_password,
                post_status=post_status, post_id=post_id, post_type=post_type  # Pass post_type
            )

            if post_result:
                if post_id: # Always an update if post_id is not None
                    print(f"Article/Page updated successfully on {full_wordpress_url} with Post ID: {post_id}")
                else:
                    print(f"Article created with ID: {post_result} on {full_wordpress_url}") #This case will be use for the creation of post.
            else:
                print(f"Failed to create or update article on {full_wordpress_url}")


            time.sleep(int(sleep_time))

        except Exception as e:
            print(f"--- 💥 Error processing URL: {provided_url}, Keyword: {query} ---")
            print(f"Error details: {e}")
            print("Moving to the next entry...")

    print("--- End of Operations ---")
from django.shortcuts import render
from .forms import GeneralConfigForm, OpenAIConfigForm, WordPressConfigForm, SiteKeywordForm 
from .utils import config_utils  # Import the config_utils module, 
import json # Import the json module
import csv
import time
def dashboard_view(request):
    # Load initial configurations from JSON files
    initial_general_config = config_utils.load_general_config()
    initial_openai_config = config_utils.load_openai_config()
    initial_wordpress_config = config_utils.load_wordpress_config()

    general_form = GeneralConfigForm(initial=initial_general_config) # Initialize forms with loaded data
    openai_form = OpenAIConfigForm(initial=initial_openai_config)
    wordpress_form = WordPressConfigForm(initial=initial_wordpress_config)
    
    # --- Load sites_keywords data using config_utils ---
    sites_keywords_data = config_utils.load_sites_keywords() # Load using the new function
    
    site_keyword_form = SiteKeywordForm() # Create an instance of SiteKeywordForm

    if request.method == 'POST':
        print("Request method is POST")
        print("request.FILES:", request.FILES)
        print("request:", request)
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
            print('ujnhbvc')
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

    context = {
        'general_form': general_form,
        'openai_form': openai_form,
        'wordpress_form': wordpress_form,
        'sites_keywords': sites_keywords_data,
        'site_keyword_form': site_keyword_form,
    }
    return render(request, 'ghost_app/index.html', context)
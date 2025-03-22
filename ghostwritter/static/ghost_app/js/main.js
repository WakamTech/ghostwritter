document.addEventListener('DOMContentLoaded', function() {
    // For JSON Config Import Form
    const importConfigFileInput = document.getElementById('import-config-file');
    if (importConfigFileInput) { // Check if the element exists on the page
        importConfigFileInput.addEventListener('change', function() {
            const form = document.getElementById('import-config-form');
            if (form) {
                form.submit(); // Submit the form when a file is selected
            }
        });
    }

    // For CSV Sites/Keywords Import Form
    const importSitesKeywordsCsvInput = document.getElementById('import-sites-keywords-csv');
    if (importSitesKeywordsCsvInput) { // Check if the element exists on the page
        importSitesKeywordsCsvInput.addEventListener('change', function() {
            const form = document.getElementById('import-sites-keywords-csv-form');
            if (form) {
                form.submit(); // Submit the form when a file is selected
            }
        });
    }
});
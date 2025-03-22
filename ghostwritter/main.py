import os
import sys

def get_base_path():
    # Récupérer le chemin correct dans l'exécutable
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS  # Chemin temporaire utilisé par PyInstaller
    return os.path.dirname(os.path.abspath(__file__))

def main():
    base_path = get_base_path()

    # Adapter les chemins dans les settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ghostwritter.settings')
    os.environ['DJANGO_BASE_PATH'] = base_path

    from django.core.management import execute_from_command_line
    execute_from_command_line(['manage.py', 'runserver', '0.0.0.0:8000', '--noreload'])

if __name__ == '__main__':
    main()

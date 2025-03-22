"""
Django settings for ghostwritter project.
... (le reste de votre fichier settings.py) ...
"""

from pathlib import Path
import os
import sys

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-flc%)yk@xmhd8czn&a0x_x6p@#)t2uh$m1aou0@d5*e(v6wdh-'
DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ghost_app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ghostwritter.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

STATIC_URL = '/static/'

# Chemin vers les fichiers statiques pendant le développement
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    # Exécution dans un exécutable PyInstaller
    STATICFILES_DIRS = [
        os.path.join(sys._MEIPASS, 'static'),
    ]
else:
    # Exécution en mode développement normal
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'static'), # Si vous avez un dossier 'static' à la racine pour des fichiers globaux
        os.path.join(BASE_DIR, 'ghost_app', 'static'), # Le dossier static de votre application
    ]

# Emplacement de collecte pour la production (répertoire séparé)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') # Utiliser 'staticfiles'

TEMPLATES[0]['DIRS'] = [os.path.join(BASE_DIR, 'templates')]
WSGI_APPLICATION = 'ghostwritter.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
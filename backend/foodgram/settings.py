from os import environ, path
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()
path.expanduser('~')

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = environ.get('DEBUG', default=True)

SECRET_KEY = environ.get('SECRET_KEY', default='delete this default')

ALLOWED_HOSTS = environ.get(
    'ALLOWED_HOSTS', default='127.0.0.1, localhost'
).split(', ')

CSRF_TRUSTED_ORIGINS = environ.get(
    'CSRF_TRUSTED_ORIGINS', default='http://localhost, http://127.0.0.1'
).split(', ')

ROOT_URLCONF = 'foodgram.urls'

WSGI_APPLICATION = 'foodgram.wsgi.application'

AUTH_USER_MODEL = 'users.MyUser'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'djoser',
    'django_filters',
    'api.apps.ApiConfig',
    'recipes.apps.RecipesConfig',
    'users.apps.UsersConfig',
    'django_extensions',
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

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

DATABASES = {
    'default': {
        'ENGINE': environ.get(
            'DB_ENGINE', default='django.db.backends.postgresql'),
        'NAME': environ.get(
            'DB_NAME', default='postgres'),
        'USER': environ.get(
            'POSTGRES_USER', default='postgres'),
        'PASSWORD': environ.get(
            'POSTGRES_PASSWORD', default='password'),
        'HOST': environ.get(
            'DB_HOST', default='db'),
        'PORT': environ.get(
            'DB_PORT', default=5432)
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME':
     'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    {'NAME':
     'django.contrib.auth.password_validation.MinimumLengthValidator', },
    {'NAME':
     'django.contrib.auth.password_validation.CommonPasswordValidator', },
    {'NAME':
     'django.contrib.auth.password_validation.NumericPasswordValidator', },
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES':
    ['rest_framework.permissions.IsAuthenticatedOrReadOnly', ],

    'DEFAULT_AUTHENTICATION_CLASSES':
    ['rest_framework.authentication.TokenAuthentication', ],

    'DEFAULT_PAGINATION_CLASS':
    'rest_framework.pagination.PageNumberPagination',

    'PAGE_SIZE': 6
}

DJOSER = {
    'LOGIN_FIELD': 'email',
    'HIDE_USERS': False,
    'PERMISSIONS': {
        'resipe': ('rest_framework.permissions.AllowAny',),
        'recipe_list': ('rest_framework.permissions.AllowAny',),
        'user': ('rest_framework.permissions.AllowAny',),
        'user_list': ('rest_framework.permissions.AllowAny',),
    },
    'SERIALIZERS': {
        'user': 'api.serializers.UserSerializer',
        'user_list': 'api.serializers.UserSerializer',
        'current_user': 'api.serializers.UserSerializer',
        'user_create': 'api.serializers.UserSerializer',
    },
}

LANGUAGE_CODE = 'ru'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / STATIC_URL

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / MEDIA_URL

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# for review
if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': str(BASE_DIR / 'db.sqlite3'),
        }
    }

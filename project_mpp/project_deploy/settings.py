"""
Django settings for project_deploy project.

Generated by 'django-admin startproject' using Django 3.2.9.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os
from pathlib import Path
from datetime import timedelta

import pdfkit

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

from os import environ
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')

load_dotenv(dotenv_path)


# Application definition

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = environ.get('SECRET_KEY')


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'app_deploy',
    'app_usuario',
    'app_licfunc',
    'app_contribuyente',
    'app_rrhh',
    'app_planif',
    'app_tradoc',
    'app_tesorero',
    'app_abastec',
    'app_siaf',
    "rest_framework",
    'corsheaders'
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    "django.middleware.common.CommonMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',    
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project_deploy.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS':  [BASE_DIR / 'app_licfunc' / 'templates'],
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

WSGI_APPLICATION = 'project_deploy.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
        'default': {
            'ENGINE': 'mssql',
            'NAME': environ.get('DB_NAME'),
            'USER': environ.get('DB_USERNAME'),
            'PASSWORD': environ.get('DB_PASSWORD'),
            'HOST': environ.get('DB_HOST'),
            'PORT': '',

            'OPTIONS': {
                'driver': 'ODBC Driver 17 for SQL Server',
            },
        },
        'BDSIAT': {
            'ENGINE': 'mssql',
            'NAME': environ.get('DB_SIAT'),
            'USER': environ.get('DB_USERNAME'),
            'PASSWORD': environ.get('DB_PASSWORD'),
            'HOST': environ.get('DB_HOST'),
            'PORT': '',

            'OPTIONS': {
                'driver': 'ODBC Driver 17 for SQL Server',
            },
        },        
        'BDSIGA': {
            'ENGINE': 'mssql',
            'NAME': environ.get('DB_SIGA'),
            'USER': environ.get('DB_USERNAME'),
            'PASSWORD': environ.get('DB_PASSWORD'),
            'HOST': environ.get('DB_HOST'),
            'PORT': '',

            'OPTIONS': {
                'driver': 'ODBC Driver 17 for SQL Server',
            },
        },

   }

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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

AUTH_USER_MODEL = 'app_usuario.UsuarioModel'

AUTHENTICATION_BACKENDS = ( 'app_usuario.auth.MyBackend','django.contrib.auth.backends.ModelBackend',)


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'es-pe'

TIME_ZONE = 'America/Lima'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

# brinda toda la configuracion necesaria a mi libreria de DJANGO REST FRAMEWORK
REST_FRAMEWORK = {
    # sirve para indicar que la clase encargada de la authenticacion de las rutas de mi API REST las realizara la libreria rest_framework_simplejwt
    'DEFAULT_AUTHENTICATION_CLASSES': (            
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 2,
}
# encargada de la configuracion de mi libreria de DRF SIMPLE JWT
SIMPLE_JWT = {
    'USER_ID_FIELD': 'username',
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=12),
}

STATIC_URL = '/static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#CORS_ALLOWED_ORIGINS = ["http://localhost:3000"]
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE"]
CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]

EMAIL_BACKEND = environ.get('EMAIL_BACKEND')
EMAIL_HOST = environ.get('EMAIL_HOST')
EMAIL_PORT = environ.get('EMAIL_PORT')
EMAIL_USE_TLS = environ.get('EMAIL_USE_TLS')
EMAIL_HOST_USER = environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = environ.get('EMAIL_HOST_PASSWORD')
RECIPIENT_ADDRESS= environ.get('RECIPIENT_ADDRESS')

# FILE_UPLOAD_PERMISSIONS = 770
# FILE_UPLOAD_DIRECTORY_PERMISSIONS =770

WKHTMLTOPDF_CMD = 'C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe'
PDFKIT_CONFIG = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_CMD)
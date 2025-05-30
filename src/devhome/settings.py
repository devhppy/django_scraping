# """
# Django settings for devhome project.

# Generated by 'django-admin startproject' using Django 5.2.

# For more information on this file, see
# https://docs.djangoproject.com/en/5.2/topics/settings/

# For the full list of settings and their values, see
# https://docs.djangoproject.com/en/5.2/ref/settings/
# """

# import base64
# import tempfile
# import os

# from pathlib import Path
# from decouple import config

# from cassandra import ConsistencyLevel
# from cassandra.cluster import Cluster
# from cassandra.auth import PlainTextAuthProvider
# # Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve().parent.parent


# # Quick-start development settings - unsuitable for production
# # See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# # SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = config("DJANGO_SECRET_KEY", default=None)

# # SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = config("DEBUG", default=False, cast=bool)

# # Decode Secure_Connect.zip from base64 if provided
# ASTRA_BUNDLE_B64 = config("ASTRA_BUNDLE_B64", default=None)

# if ASTRA_BUNDLE_B64:
#     decoded_zip_path = os.path.join(tempfile.gettempdir(), "secure_connect_bundle.zip")
#     with open(decoded_zip_path, "wb") as f:
#         f.write(base64.b64decode(ASTRA_BUNDLE_B64))
#     SECURE_CONNECT_BUNDLE_PATH = decoded_zip_path
# # else:
# #     # fallback for local dev or manual mount
# #     SECURE_CONNECT_BUNDLE_PATH = config("ASTRA_BUNDLE_PATH", default="Secure_Connect.zip")

# ALLOWED_HOSTS = []


# # Application definition

# INSTALLED_APPS = [
#     'django.contrib.admin',
#     'django.contrib.auth',
#     'django.contrib.contenttypes',
#     'django.contrib.sessions',
#     'django.contrib.messages',
#     'django.contrib.staticfiles',
#     # My Apps
#     "django_celery_beat",
#     "django_celery_results",
#     "movies",
#     "products"
# ]


# INSTALLED_APPS = ["django_cassandra_engine"] + INSTALLED_APPS

# SESSION_ENGINE = "django_cassandra_engine.sessions.backends.db"

# MIDDLEWARE = [
#     'django.middleware.security.SecurityMiddleware',
#     'django.contrib.sessions.middleware.SessionMiddleware',
#     'django.middleware.common.CommonMiddleware',
#     'django.middleware.csrf.CsrfViewMiddleware',
#     'django.contrib.auth.middleware.AuthenticationMiddleware',
#     'django.contrib.messages.middleware.MessageMiddleware',
#     'django.middleware.clickjacking.XFrameOptionsMiddleware',
# ]

# ROOT_URLCONF = 'devhome.urls'

# TEMPLATES = [
#     {
#         'BACKEND': 'django.template.backends.django.DjangoTemplates',
#         'DIRS': [],
#         'APP_DIRS': True,
#         'OPTIONS': {
#             'context_processors': [
#                 'django.template.context_processors.request',
#                 'django.contrib.auth.context_processors.auth',
#                 'django.contrib.messages.context_processors.messages',
#             ],
#         },
#     },
# ]

# WSGI_APPLICATION = 'devhome.wsgi.application'


# # Database
# # https://docs.djangoproject.com/en/5.2/ref/settings/#databases

# # DATABASES = {
# #     'default': {
# #         'ENGINE': 'django.db.backends.sqlite3',
# #         'NAME': BASE_DIR / 'db.sqlite3',
# #     }
# # }

# DATABASES = {
#     'default': {
#         'ENGINE': 'django_cassandra_engine',
#         'NAME': config('ASTRA_KEY_SPACE', default='devhome', cast=str),
#         'OPTIONS':{
#             'connection':{
#                 'auth_provider': PlainTextAuthProvider(
#                     config('ASTRA_CLIENT_ID', default='cassandra', cast=str),
#                     config('ASTRA_CLIENT_SECRET', default='cassandra', cast=str),
#                 ),
#                 'consistency': 'LOCAL_QUORUM',
#                 'retry_connect': True,
#                 'cloud': {
#                     'secure_connect_bundle': SECURE_CONNECT_BUNDLE_PATH
#                 }
#             }
#         }
#     }
# }


# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'console': {
#             'class': 'logging.StreamHandler',
#         },
#     },
#     'root': {
#         'handlers': ['console'],
#         'level': 'INFO',
#     },
# }

# # Password validation
# # https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

# AUTH_PASSWORD_VALIDATORS = [
#     {
#         'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
#     },
# ]


# # Internationalization
# # https://docs.djangoproject.com/en/5.2/topics/i18n/

# LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'UTC'

# USE_I18N = True

# USE_TZ = True


# # Static files (CSS, JavaScript, Images)
# # https://docs.djangoproject.com/en/5.2/howto/static-files/

# STATIC_URL = 'static/'

# # Default primary key field type
# # https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

# DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# # save Celery task results in Django's database
# CELERY_RESULT_BACKEND = "django-db"

# # broker_connection_retry_on_startup
# CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

# CELERY_BROKER_URL = config('CELERY_BROKER_REDIS_URL', default='redis://localhost:6379/0')

# # this allows you to schedule items in the Django admin.
# CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers.DatabaseScheduler"

import base64
import os
import tempfile
from pathlib import Path

from cassandra.auth import PlainTextAuthProvider
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config("DJANGO_SECRET_KEY")
DEBUG      = config("DEBUG", default=False, cast=bool)

ALLOWED_HOSTS = []

# ——— Cassandra (Astra) DB for application data ———
ASTRA_BUNDLE_B64    = config("ASTRA_BUNDLE_B64")
ASTRA_CLIENT_ID     = config("ASTRA_CLIENT_ID")
ASTRA_CLIENT_SECRET = config("ASTRA_CLIENT_SECRET")
ASTRA_KEYSPACE      = config("ASTRA_KEY_SPACE", default="products_db")

# write the secure connect bundle to a temp file
bundle_path = os.path.join(tempfile.gettempdir(), "secure_connect_bundle.zip")
with open(bundle_path, "wb") as f:
    f.write(base64.b64decode(ASTRA_BUNDLE_B64))

DATABASES = {
    'cassandra': {
        'ENGINE': 'django_cassandra_engine',
        'NAME': ASTRA_KEYSPACE,
        'OPTIONS': {
            'connection': {
                'auth_provider': PlainTextAuthProvider(
                    ASTRA_CLIENT_ID,
                    ASTRA_CLIENT_SECRET,
                ),
                'cloud': {
                    'secure_connect_bundle': bundle_path,
                },
                'consistency': 'LOCAL_QUORUM',
                'retry_connect': True,
            }
        }
    },
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',             # or use postgresql_psycopg2 in prod
        'NAME': BASE_DIR / 'celerybeat.sqlite3',
    },
}

# Router to send cassandra models to default_cassandra, and django-celery apps to default_sql
# DATABASE_ROUTERS = ['django_cassandra_engine.router.CassandraSyncRouter']
DATABASE_ROUTERS = ['devhome.database_router.CassandraRouter']

# ——— Installed apps ———
INSTALLED_APPS = [
    # Django core
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Celery/Beat + Results (use SQL backend)
    'django_celery_beat',       # periodic task scheduling
    'django_celery_results',    # task result store

    # Your apps
    'movies',
    'products',
]

# Ensure cassandra engine comes first when resolving ENGINE strings
INSTALLED_APPS.insert(0, 'django_cassandra_engine')

SESSION_ENGINE = "django_cassandra_engine.sessions.backends.db"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'devhome.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'devhome.wsgi.application'


# ——— Celery Configuration ———

CELERY_BROKER_URL                        = config('CELERY_BROKER_REDIS_URL', default='redis://localhost:6379/0')
CELERY_RESULT_BACKEND                    = 'django-db'    # store task results in SQL DB
CELERY_ACCEPT_CONTENT                    = ['json']
CELERY_TASK_SERIALIZER                   = 'json'
CELERY_RESULT_SERIALIZER                 = 'json'
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP= True

# Use django-celery-beat’s scheduler (stores schedule in SQL)
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'


from datetime import timedelta

CELERY_BEAT_SCHEDULE = {
    # run every 5 minutes (adjust as needed)
    'sync-google-sheets-every-5-minutes': {
        'task': 'products.tasks.process_google_sheet_data',
        'schedule': timedelta(minutes=2),
        # optional: pass args if your task signature requires them
        # 'args': (),
    },
}

# ——— Logging ———

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {'class': 'logging.StreamHandler'},
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}

# ——— Internationalization & Static ———

LANGUAGE_CODE = 'en-us'
TIME_ZONE     = 'UTC'
USE_I18N      = True
USE_TZ        = True
STATIC_URL    = '/static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

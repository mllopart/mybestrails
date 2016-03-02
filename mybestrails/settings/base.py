# -*- coding: utf-8 -*-
"""
Django settings for mybestrails project.
"""

import os
import json
import dj_database_url
from django.core.exceptions import ImproperlyConfigured
from os.path import join, abspath, dirname

#dirs
here = lambda *dirs: join(abspath(dirname(__file__)), *dirs)
BASE_DIR = here("..", "..")
root = lambda *dirs: join(abspath(BASE_DIR), *dirs)

# JSON-based secrets module
with open("secrets.json") as f:
    secrets = json.loads(f.read())

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = os.environ.get('SECRET_KEY', 'H/wOg04Nt*6Oo}91k^H*5E}8Mbo4p"')

DEBUG = bool(os.environ.get('DEBUG', False))

ADMINS = (
    ('Marc Llopart', 'larsnow@gmail.com'),
)

MANAGERS = (
    ('Marc Llopart', 'larsnow@gmail.com'),
)

# Application definition    
INSTALLED_APPS = [
    'app.core.apps.CoreConfig',
    'app.track_management.apps.TrackManagementConfig',
    'app.user_management.apps.UserManagementConfig',
    'app.logger_management.apps.LoggerManagementConfig',
    'app.general.apps.GeneralConfig',   
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',    
]

INSTALLED_APPS += ('tastypie',
                   'storages',
                   'social.apps.django_app.default',)


MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mybestrails.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, "templates/"),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.core.context_processors.i18n',
                'django.core.context_processors.media',
                'django.core.context_processors.static',
                'django.core.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'social.apps.django_app.context_processors.backends',
                'social.apps.django_app.context_processors.login_redirect',
            ],
        },
    },
             
    #{
    #    'BACKEND': 'django.template.backends.jinja2.Jinja2',
    #    'APP_DIRS': True,
    #    'DIRS': [
    #        '/home/html/jinja2',
    #    ],
    #},
]

AUTHENTICATION_BACKENDS = (
    'social.backends.facebook.FacebookOAuth2',
    #'social.backends.open_id.OpenIdAuth',
    #'social.backends.google.GoogleOpenId',
    #'social.backends.google.GoogleOAuth2',
    #'social.backends.google.GoogleOAuth',
    #'social.backends.twitter.TwitterOAuth',
    #'social.backends.yahoo.YahooOpenId',
    'django.contrib.auth.backends.ModelBackend',
)

WSGI_APPLICATION = 'mybestrails.wsgi.application'

#SOCIAL
LOGIN_REDIRECT_URL = '/'

SOCIAL_AUTH_FACEBOOK_KEY = get_env_variable('SOCIAL_AUTH_FACEBOOK_KEY')
SOCIAL_AUTH_FACEBOOK_SECRET = get_env_variable('SOCIAL_AUTH_FACEBOOK_SECRET')

# Database
DATABASES = {}
db_from_env = dj_database_url.config()
DATABASES['default'].update(db_from_env)
DATABASES['default']['ENGINE'] = 'django.contrib.gis.db.backends.postgis'


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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

#logger
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/home/mllopart/workspace/mybestrailsEnv/debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

 

# Static files (CSS, JavaScript, Images)

#AWS settings
AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
AWS_S3_CUSTOM_DOMAIN = 's3.amazonaws.com/%s' % AWS_STORAGE_BUCKET_NAME
#AWS_HEADERS = {
#    'Expires': 'Thu, 15 Apr 2010 20:00:00 GMT',
#    'Cache-Control': 'max-age=86400',
#}


STATICFILES_FINDERS = ["django.contrib.staticfiles.finders.FileSystemFinder",
 "django.contrib.staticfiles.finders.AppDirectoriesFinder"]
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)


STATICFILES_LOCATION = 'static'
#STATICFILES_STORAGE = 'lib.custom_storages.StaticStorage'
STATIC_URL = "http://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, STATICFILES_LOCATION)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

MEDIAFILES_LOCATION = 'media'
DEFAULT_FILE_STORAGE = 'lib.custom_storages.MediaStorage'
MEDIA_URL = "http://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, MEDIAFILES_LOCATION)


#STATICFILES_DIRS = (os.path.join(BASE_DIR, "static/"),)
#STATIC_URL = '/static/'
TMP_MEDIA_ROOT = os.path.join(BASE_DIR, "media_tmp/")

def get_env_variable(var_name):
	"""Get the environment variable or return exception."""
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = "Set the {} environment variable".format(var_name)
        raise ImproperlyConfigured(erro.r_msg)
        

    
def get_secret(setting, secrets=secrets):
    """Get the secret variable or return explicit exception."""
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {0} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)

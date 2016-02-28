# -*- coding: utf-8 -*-
"""
Django settings for mybestrails project.

Generated by 'django-admin startproject' using Django 1.9.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
import dj_database_url

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '2$$gaofcyir+a9ek&ns&1)33bf=f=^a_1)v68=!r8_z3&yj4$0'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

ADMINS = (
    ('Marc Llopart', 'larsnow@gmail.com'),
)

MANAGERS = (
    ('Marc Llopart', 'larsnow@gmail.com'),
)

GOOGLE_ANALYTICS_CODE = 'UA-74107701-1'


# Application definition
    
INSTALLED_APPS = [
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
                   'debug_toolbar',
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

SOCIAL_AUTH_FACEBOOK_KEY = '1052351271473390'
SOCIAL_AUTH_FACEBOOK_SECRET = '50e47604b2e60b0a3d1476932f2ef332' 

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.contrib.gis.db.backends.postgis',
#        'NAME': 'mybestrails',
#        'USER': 'mybestrailsdba',
#        'PASSWORD': 'C#az3Xg8CE@qRD',
#        'HOST': 'localhost',
#        'PORT': '',
#    }
#}

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
# https://docs.djangoproject.com/en/1.9/howto/static-files/

#AWS settings
AWS_STORAGE_BUCKET_NAME = 'mybestrails'
AWS_ACCESS_KEY_ID = 'AKIAJOIXLF3C3PBXI6OQ'
AWS_SECRET_ACCESS_KEY = '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'
AWS_S3_CUSTOM_DOMAIN = 's3.amazonaws.com/%s' % AWS_STORAGE_BUCKET_NAME
#AWS_HEADERS = {
#    'Expires': 'Thu, 15 Apr 2010 20:00:00 GMT',
#    'Cache-Control': 'max-age=86400',
#}


STATICFILES_FINDERS = ["django.contrib.staticfiles.finders.FileSystemFinder",
 "django.contrib.staticfiles.finders.AppDirectoriesFinder"]
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)


STATICFILES_LOCATION = 'static'
STATICFILES_STORAGE = 'lib.custom_storages.StaticStorage'
STATIC_URL = "http://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, STATICFILES_LOCATION)

MEDIAFILES_LOCATION = 'media_dev'
DEFAULT_FILE_STORAGE = 'lib.custom_storages.MediaStorage'
MEDIA_URL = "http://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, MEDIAFILES_LOCATION)


#STATICFILES_DIRS = (os.path.join(BASE_DIR, "static/"),)
#STATIC_URL = '/static/'
TMP_MEDIA_ROOT = os.path.join(BASE_DIR, "media_tmp/")

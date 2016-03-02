# -*- coding: utf-8 -*-

# settings/local.py
from .base import *
import os
import dj_database_url

SECRET_KEY = 'Zr+$Tr2biv0GN5>F):|*E@AmHXPnsa'

DEBUG = True

ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS += ("debug_toolbar", )

#SOCIAL
SOCIAL_AUTH_FACEBOOK_KEY = '1052351271473390'
SOCIAL_AUTH_FACEBOOK_SECRET = '50e47604b2e60b0a3d1476932f2ef332' 

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'mybestrails',
        'USER': 'mybestrailsdba',
        'PASSWORD': 'C#az3Xg8CE@qRD',
        'HOST': 'localhost',
        'PORT': '',
    }
}

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

# Static files (CSS, JavaScript, Images)

#AWS settings
AWS_STORAGE_BUCKET_NAME = 'mybestrails'
AWS_ACCESS_KEY_ID = 'AKIAJOIXLF3C3PBXI6OQ'
AWS_SECRET_ACCESS_KEY = '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'

MEDIAFILES_LOCATION = 'media_dev'
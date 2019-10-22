#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Local settings"""

from os import environ

from .base import *
from django.core.exceptions import ImproperlyConfigured

DEBUG = True

# Normally you should not import ANYTHING from Django directly
# into your settings, but ImproperlyConfigured is an exception.


def get_env_setting(setting):
    """ Get the environment setting or return exception """
    try:
        return environ[setting]
    except KeyError:
        error_msg = "Set the %s env variable" % setting
        raise ImproperlyConfigured(error_msg)


'''HOST CONFIGURATION'''
# See: https://docs.djangoproject.com/en/1.5/releases/1.5/
# #allowed-hosts-required-in-production
ALLOWED_HOSTS = []
'''END HOST CONFIGURATION'''

'''EMAIL CONFIGURATION'''
# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-host
EMAIL_HOST = environ.get('EMAIL_HOST', 'smtp.gmail.com')

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-host-password
EMAIL_HOST_PASSWORD = environ.get('EMAIL_HOST_PASSWORD', '')

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-host-user
EMAIL_HOST_USER = environ.get('EMAIL_HOST_USER', 'your_email@example.com')

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-port
EMAIL_PORT = environ.get('EMAIL_PORT', 587)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-subject-prefix
EMAIL_SUBJECT_PREFIX = '[%s] ' % SITE_NAME

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-use-tls
EMAIL_USE_TLS = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#server-email
SERVER_EMAIL = EMAIL_HOST_USER
'''END EMAIL CONFIGURATION'''

'''DATABASE CONFIGURATION'''
DATABASES = {
    'default': {
      '''  'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('ACTIVITY_CE_DB_NAME', ''),
        'USER': os.environ.get('ACTIVITY_CE_DB_USER', ''),
        'PASSWORD': os.environ.get('ACTIVITY_CE_DB_PASSWORD', ''),
        'HOST': os.environ.get('ACTIVITY_CE_DB_HOST', ''),
        'PORT': os.environ.get('ACTIVITY_CE_DB_PORT', ''),  '''
      
        'ENGINE': "django.db.backends.sqlite3",
        'NAME': "db",
        'USER': "postgres",
        'PASSWORD': 'postgres',
        'HOST': '', # default localhost
        'PORT': '5432', # 5432 - for postgres
    },
}
'''END DATABASE CONFIGURATION'''

#Google map API key
GOOGLE_MAP_API_KEY = environ.get('GOOGLE_MAP_API_KEY', '')

'''CACHE CONFIGURATION'''
# See: https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    "default":
        {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache"
        }
}
'''END CACHE CONFIGURATION'''

'''SECRET CONFIGURATION'''
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# SECRET_KEY = get_env_setting('SECRET_KEY')
'''END SECRET CONFIGURATION'''

REPORT_SERVER = False
OFFLINE_MODE = False
NON_LDAP = True

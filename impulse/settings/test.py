import os

from .base import *

# A basic database set-up for Travis CI. The set-up uses the 'TRAVIS'
# environment variable on Travis to detect the session, and changes the default
# database accordingly.
DEBUG = True

if 'TRAVIS' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'travisci',
            'USER': 'postgres',
            'PASSWORD': '',
            'HOST': 'localhost',
            'PORT': '',
        }
    }

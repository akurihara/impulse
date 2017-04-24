from .base import *

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'impulse',
        'USER': 'alexkurihara',
        'PASSWORD': 'foobar',
        'HOST': 'localhost',
        'PORT': '',
    }
}

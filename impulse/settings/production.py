from .base import *

import dj_database_url

DEBUG = False

ALLOWED_HOSTS = ['.herokuapp.com']

ADMINS = [('Alex', 'alex.kurihara@gmail.com')]

db_from_envronment = dj_database_url.config()
DATABASES = {
    'default': db_from_envronment
}

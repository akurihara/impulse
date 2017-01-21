from .base import *

import dj_database_url

db_from_envronment = dj_database_url.config()
DATABASES = {
    'default': db_from_envronment
}

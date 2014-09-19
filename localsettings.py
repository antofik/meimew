import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = '1ylqmvt^z9b_#jrysgv-51ki^52fhr#els$j54hjhb5_2%g7qe'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
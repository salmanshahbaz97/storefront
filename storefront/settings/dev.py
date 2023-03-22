from .common import *


DEBUG = True

SECRET_KEY = 'django-insecure-0nyluj6$w@9ny#f$qd#@#l^3k$)0-avv#_5#+ym3z$)g_dr6(e'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'storefront',
        'HOST': 'localhost',
        'USER': 'root',
        'PASSWORD': 'salman.123'
    }
}


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

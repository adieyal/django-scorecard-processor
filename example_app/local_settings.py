from settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'testing.db',                      # Or path to database file if using
    }
}

STATICFILES_DIRS = (
    'static/',
)

MIDDLEWARE_CLASSES = ('debug_toolbar.middleware.DebugToolbarMiddleware',) + MIDDLEWARE_CLASSES
INTERNAL_IPS = ('127.0.0.1',)
INSTALLED_APPS  = INSTALLED_APPS+('debug_toolbar',)


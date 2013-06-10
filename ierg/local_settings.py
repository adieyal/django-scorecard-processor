DEBUG = True
TEMPLATE_DEBUG = DEBUG


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'coia',                      # Or path to database file if using
        'USER' : 'coia',
        'PASSWORD' : 'A1aaaaa',
    }
}


MEDIA_ROOT = '/home/coia/webapps/static/media'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/uploads/'

STATIC_URL = '/static/'
STATIC_ROOT = '/home/coia/webapps/static/static'

STATICFILES_DIRS = (
    'static/',
)

#INSTALLED_APPS  = INSTALLED_APPS+('debug_toolbar',)
#MIDDLEWARE_CLASSES = ('debug_toolbar.middleware.DebugToolbarMiddleware',) + MIDDLEWARE_CLASSES
INTERNAL_IPS = ('127.0.0.1',)

DEBUG_TOOLBAR_CONFIG = {
   "INTERCEPT_REDIRECTS":False,
   "SQL_DUPLICATES":True,
#    "ENABLE_STACKTRACES":False,
}

DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.version.VersionDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
    'debug_toolbar.panels.signals.SignalDebugPanel',
    'debug_toolbar.panels.logger.LoggingPanel',
    )

CACHES = {
    'default': {
            #'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'unique-snowflake',
    }
}

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'survey2012@ihpresults.net'
EMAIL_HOST_PASSWORD = 'surveytools'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

SERVER_EMAIL='"IHP+Results Survey 2012" <survey2012@ihpresults.net>'
DEFAULT_FROM_EMAIL=SERVER_EMAIL
ADMINS = (
    ('Sysadmin','sysadmin@ihpresults.net'),
)
EMAIL_SUBJECT_PREFIX='[Local] '

    

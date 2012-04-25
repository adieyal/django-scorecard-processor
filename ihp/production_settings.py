from settings import *
from bundle_config import config

DEBUG=False
TEMPLATE_DEBUG=DEBUG

CACHES = {
  'default': {
    'BACKEND': 'redis_cache.RedisCache',
    'LOCATION': '%s:%s' % (config['redis']['host'], config['redis']['port']),
    'OPTIONS': {
      'DB': 1,
      'PASSWORD': config['redis']['password'],
      'PARSER_CLASS': 'redis.connection.PythonParser'
    },
  },
}
CACHE_MIDDLEWARE_ANONYMOUS_ONLY=True


MIDDLEWARE_CLASSES = ("ihp_results.middleware.DomainRedirectMiddleware",) + MIDDLEWARE_CLASSES

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
MANAGERS = ADMINS
EMAIL_SUBJECT_PREFIX='[Production] '


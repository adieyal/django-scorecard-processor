from settings import *
from bundle_config import config

ADMIN_MEDIA_PREFIX = "/static/grappelli/"

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

MIDDLEWARE_CLASSES = ("ihp_results.middleware.DomainRedirectMiddleware",) + MIDDLEWARE_CLASSES

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'survey2012@ihpresults.net'
EMAIL_HOST_PASSWORD = '7813258ef8c6b632dde8cc80f6bda62f'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

SERVER_EMAIL='"IHP+Results Survey 2012" <survey2012@ihpresults.net>'
DEFAULT_FROM_EMAIL=SERVER_EMAIL
ADMINS = (
    ('Sysadmin','sysadmin@ihpresults.net'),
)
EMAIL_SUBJECT_PREFIX='[Production] '


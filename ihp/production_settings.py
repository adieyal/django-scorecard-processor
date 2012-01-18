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


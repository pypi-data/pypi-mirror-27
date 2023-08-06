# coding: utf-8
from .base import *

if not os.path.isdir('data'):
    os.mkdir('data')
REDIS_DB_PATH = os.path.join('data/redis.db')
rdb = Redis(REDIS_DB_PATH)
REDIS_SOCKET_PATH = 'redis+socket://%s' % (rdb.socket_file,)
CELERY_BROKER_URL = REDIS_SOCKET_PATH

FIXTURE_DIRS = [os.path.join(BASE_DIR, 'tests/djotali/fixtures/'), ]
DATABASES = {
    'default': dj_database_url.parse('sqlite:///:memory:', conn_max_age=600)
}
EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'

CONSOLE_SMS_MAX_TIMEOUT = 0.01
CONSOLE_SMS_MIN_TIMEOUT = 0.001

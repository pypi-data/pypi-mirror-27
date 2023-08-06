# coding: utf-8
from decouple import Csv

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

INSTALLED_APPS += [
    'debug_toolbar',
]

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

# DebugBar
DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
]

CONFIG_DEFAULTS = {
    # Toolbar options
    'RESULTS_CACHE_SIZE': 3,
    'SHOW_COLLAPSED': True,
    # Panel options
    'SQL_WARNING_THRESHOLD': 100,  # milliseconds
}

DEFAULT_DB_URL = config('DB_URL', default='mysql://root:root@127.0.0.1:3306/djotali')

DATABASES = {
    'default': dj_database_url.config(default=DEFAULT_DB_URL, conn_max_age=600)
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv(), default='*')

INTERNAL_IPS = ['127.0.0.1']

# Custom settings
ATOM_PARK_PUBLIC_KEY = config('ATOM_PARK_PUBLIC_KEY', 'dummy')
ATOM_PARK_PRIVATE_KEY = config('ATOM_PARK_PRIVATE_KEY', 'dummy')

# Celery
if not os.getenv('DEV'):
    BROKER_HOST = config('REDIS_HOST', default='127.0.0.1')
    BROKER_PORT = config('REDIS_PORT', default=6379)
    CELERY_BROKER_URL = config('CELERY_BROKER_URL', default='redis://{}:{}/0'.format(BROKER_HOST, BROKER_PORT))

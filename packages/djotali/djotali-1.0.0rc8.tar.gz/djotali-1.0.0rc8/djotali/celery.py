# coding: utf-8
import os
import sys
from multiprocessing import Process

from celery import Celery
from celery.bin.worker import worker
from django.conf import settings

from djotali.core.utils import is_celery_running


def _is_standalone_launch():
    return os.getenv('DEV') and not settings.TESTING and not is_celery_running() and 'runserver' in sys.argv


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djotali.settings')

app = Celery('djotali')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


# The following code automatically launch a celery worker if in DEV mode
# It is for convenience reason and not needed otherwise as production and testing modes have other ways to start celery worker
def init_celery_worker_and_beat():
    celery_worker_thread = Process(target=lambda: worker(app=app).run(app=app, loglevel='info', beat=True))
    celery_worker_thread.daemon = True
    celery_worker_thread.start()


if _is_standalone_launch():
    init_celery_worker_and_beat()

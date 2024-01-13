import os

from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'imdb.settings')
app = Celery('imdb')
app.config_from_object('django.conf:settings', namespace='CELERY')
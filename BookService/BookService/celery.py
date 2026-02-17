import os
from celery import Celery

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'BookService.settings'
)

app = Celery('BookService')
app.conf.broker_url="redis://redis:6379/0"
app.conf.result_backend="redis://redis:6379/0"
app.conf.timezone = 'Europe/Chisinau'
app.autodiscover_tasks()
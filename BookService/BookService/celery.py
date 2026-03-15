import os
from datetime import timedelta

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'BookService.settings'
)

app = Celery('BookService')
app.conf.broker_url="redis://redis:6379/0"
app.conf.result_backend="redis://redis:6379/0"
app.conf.timezone = 'Europe/Chisinau'
app.autodiscover_tasks()

app.conf.beat_schedule = {
'generate-weekly-slots': {
         'task': 'service.tasks.generate_weekly_slots',
         'schedule': crontab(hour=0, minute=0, day_of_week='sunday'),
     },
}
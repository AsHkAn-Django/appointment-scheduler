import os
from celery import Celery
import multiprocessing

multiprocessing.set_start_method('spawn', True)  # force spawn on Windows
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'appointmentScheduler.settings')
app = Celery('appointmentScheduler')
app.config_from_object('django.conf.settings', namespace='CELERY')
app.conf.beat_scheduler = 'django_celery_beat.schedulers:DatabaseScheduler'
app.conf.timezone = 'UTC'
app.autodiscover_tasks()
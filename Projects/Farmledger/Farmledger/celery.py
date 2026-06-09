import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Farmledger.settings')

app = Celery('Farmledger')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

# Periodic tasks: schedule fetch_weather_for_all_farms hourly when Celery is available
try:
    from celery.schedules import crontab

    app.conf.beat_schedule = {
        'fetch-weather-hourly': {
            'task': 'apps.weather.tasks.fetch_weather_for_all_farms',
            'schedule': crontab(minute=0, hour='*/1'),
        },
    }
except (ImportError, ModuleNotFoundError):
    # Celery not installed or schedules unavailable in this environment
    # Explicitly catch import errors to avoid swallowing unexpected exceptions
    from logging import getLogger

    getLogger(__name__).debug("Celery not available in this environment; skipping beat schedule")

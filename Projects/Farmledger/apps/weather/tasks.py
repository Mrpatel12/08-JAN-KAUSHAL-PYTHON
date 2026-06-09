import os
import requests
from celery import shared_task
from django.conf import settings


@shared_task
def fetch_weather_for_farm(farm_id, location):
    """Fetch weather data for a given farm and store observation.

    Location can be a free-text city or coordinates; for now we pass it to
    OpenWeatherMap's 'q' parameter and fall back silently if there's no API key.
    """
    api_key = os.environ.get('OPENWEATHER_API_KEY') or getattr(settings, 'OPENWEATHER_API_KEY', None)
    if not api_key:
        return {'error': 'no_api_key'}

    url = 'https://api.openweathermap.org/data/2.5/weather'
    params = {'q': location, 'appid': api_key, 'units': 'metric'}
    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except Exception as exc:
        return {'error': str(exc)}

    # Lazy import to avoid circular imports at module import time
    from .models import WeatherObservation
    from apps.farms.models import Farm

    try:
        farm = Farm.objects.get(id=farm_id)
    except Farm.DoesNotExist:
        return {'error': 'farm_not_found'}

    WeatherObservation.objects.create(farm=farm, raw=data)
    return {'ok': True}


@shared_task
def fetch_weather_for_all_farms():
    from apps.farms.models import Farm
    farms = Farm.objects.filter(status='active')
    results = []
    for f in farms:
        loc = f.location or ''
        results.append(fetch_weather_for_farm.delay(str(f.id), loc))
    return {'dispatched': len(results)}

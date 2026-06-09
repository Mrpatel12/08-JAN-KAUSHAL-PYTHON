from django.contrib import admin
from .models import WeatherObservation


@admin.register(WeatherObservation)
class WeatherObservationAdmin(admin.ModelAdmin):
    list_display = ('farm', 'provider', 'fetched_at')
    readonly_fields = ('raw', 'fetched_at')

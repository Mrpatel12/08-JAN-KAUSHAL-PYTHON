from rest_framework import serializers
from .models import WeatherObservation


class WeatherObservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherObservation
        fields = ('id', 'farm', 'provider', 'raw', 'fetched_at')
        read_only_fields = ('raw', 'fetched_at')

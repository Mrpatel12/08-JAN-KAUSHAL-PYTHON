import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone as dj_timezone


class WeatherObservation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    farm = models.ForeignKey('farms.Farm', on_delete=models.CASCADE, related_name='weather')
    provider = models.CharField(max_length=64, default='openweathermap')
    raw = models.JSONField()
    fetched_at = models.DateTimeField(default=dj_timezone.now)

    class Meta:
        ordering = ['-fetched_at']

    def __str__(self):
        return f"Weather for {self.farm} at {self.fetched_at.isoformat()}"

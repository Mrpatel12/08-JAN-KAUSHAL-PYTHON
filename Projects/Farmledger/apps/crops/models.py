import uuid
from django.db import models
from django.utils import timezone as dj_timezone
from django.conf import settings


class Crop(models.Model):
    STATUS_CHOICES = [
        ('planned', 'Planned'),
        ('planted', 'Planted'),
        ('growing', 'Growing'),
        ('harvested', 'Harvested'),
        ('failed', 'Failed'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    farm = models.ForeignKey('farms.Farm', on_delete=models.CASCADE, related_name='crops')
    name = models.CharField(max_length=255)
    variety = models.CharField(max_length=255, blank=True)
    planted_at = models.DateField(null=True, blank=True)
    expected_harvest_at = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default='planned')
    area_planted = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    created_at = models.DateTimeField(default=dj_timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [models.Index(fields=['farm', 'status'])]

    def __str__(self):
        return f"{self.name} ({self.farm})"

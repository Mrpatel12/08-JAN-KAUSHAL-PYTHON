import uuid
from django.db import models
from django.utils import timezone as dj_timezone
from django.conf import settings


class Farm(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='farms')
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    location = models.CharField(max_length=512, blank=True)
    acreage = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    timezone = models.CharField(max_length=64, default='UTC')
    currency = models.CharField(max_length=3, default='USD')
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default='active')

    created_at = models.DateTimeField(default=dj_timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = (('owner', 'slug'),)
        indexes = [
            models.Index(fields=['owner', 'slug']),
        ]

    def __str__(self):
        return f"{self.name} ({self.owner})"

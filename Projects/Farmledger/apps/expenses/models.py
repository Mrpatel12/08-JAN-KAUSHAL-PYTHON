import uuid
from django.db import models
from django.utils import timezone as dj_timezone
from django.conf import settings


class Expense(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    farm = models.ForeignKey('farms.Farm', on_delete=models.CASCADE, related_name='expenses')
    crop = models.ForeignKey('crops.Crop', on_delete=models.SET_NULL, null=True, blank=True, related_name='expenses')
    category = models.CharField(max_length=100, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    occurred_at = models.DateTimeField(default=dj_timezone.now)
    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(default=dj_timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [models.Index(fields=['farm', 'occurred_at'])]

    def __str__(self):
        return f"Expense {self.amount} {self.currency} on {self.farm}"

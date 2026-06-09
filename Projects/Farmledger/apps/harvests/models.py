import uuid
from django.db import models
from django.utils import timezone as dj_timezone


class Harvest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    farm = models.ForeignKey('farms.Farm', on_delete=models.CASCADE, related_name='harvests')
    crop = models.ForeignKey('crops.Crop', on_delete=models.SET_NULL, null=True, blank=True, related_name='harvests')
    harvested_at = models.DateTimeField(default=dj_timezone.now)
    quantity = models.DecimalField(max_digits=12, decimal_places=3, null=True, blank=True)
    unit = models.CharField(max_length=32, default='kg')
    revenue = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(default=dj_timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [models.Index(fields=['farm', 'harvested_at'])]

    def __str__(self):
        return f"Harvest {self.quantity} {self.unit} from {self.farm}"

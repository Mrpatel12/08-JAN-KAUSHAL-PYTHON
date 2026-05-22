from django.db import models

# Create your models here.
class studinfo(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    city = models.CharField(max_length=10)
    
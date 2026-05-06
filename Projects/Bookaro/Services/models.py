from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, help_text="Emoji or FontAwesome icon name")
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

class Accommodation(models.Model):
    TYPE_CHOICES = [
        ('HOTEL', 'Hotel'),
        ('VILLA', 'Villa'),
        ('HOMESTAY', 'Homestay'),
    ]
    
    name = models.CharField(max_length=200)
    accommodation_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='HOTEL')
    location = models.CharField(max_length=200)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image_url = models.URLField(blank=True, help_text="URL to accommodation image")
    rating = models.FloatField(default=5.0)
    
    def __str__(self):
        return f"{self.name} ({self.accommodation_type})"

class Flight(models.Model):
    airline = models.CharField(max_length=100)
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_time = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    flight_number = models.CharField(max_length=20)
    
    def __str__(self):
        return f"{self.airline} - {self.flight_number} ({self.origin} to {self.destination})"

class TravelPackage(models.Model):
    name = models.CharField(max_length=200)
    destinations = models.CharField(max_length=255)
    duration_days = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image_url = models.URLField(blank=True, help_text="URL to package image")
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.name

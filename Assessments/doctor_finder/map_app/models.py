import requests
from django.db import models
from django.conf import settings

class Doctor(models.Model):
    SPECIALTY_CHOICES = [
        ('Cardiologist', 'Cardiologist'),
        ('Pediatrician', 'Pediatrician'),
        ('Dermatologist', 'Dermatologist'),
        ('Orthopedist', 'Orthopedist'),
        ('Neurologist', 'Neurologist'),
        ('General Practitioner', 'General Practitioner'),
        ('Ophthalmologist', 'Ophthalmologist'),
        ('Dentist', 'Dentist'),
    ]

    name = models.CharField(max_length=150, help_text="Full name of the doctor")
    specialty = models.CharField(max_length=50, choices=SPECIALTY_CHOICES, default='General Practitioner')
    clinic_name = models.CharField(max_length=150, help_text="Clinic or hospital name")
    address = models.CharField(max_length=300, help_text="Full physical address")
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, help_text="Latitude coordinates (auto-filled if empty and API key is set)")
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, help_text="Longitude coordinates (auto-filled if empty and API key is set)")
    phone_number = models.CharField(max_length=20, help_text="Contact number")
    email = models.EmailField(blank=True, help_text="Contact email address")
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=5.0, help_text="Rating from 1.0 to 5.0")
    website = models.URLField(blank=True, help_text="Doctor or clinic website URL")

    def __str__(self):
        return f"Dr. {self.name} - {self.specialty}"

    def save(self, *args, **kwargs):
        # Auto-geocode if coordinates are missing and address is present
        if (self.latitude is None or self.longitude is None) and self.address:
            api_key = getattr(settings, 'GOOGLE_MAPS_API_KEY', '')
            if api_key:
                try:
                    url = "https://maps.googleapis.com/maps/api/geocode/json"
                    params = {
                        "address": self.address,
                        "key": api_key
                    }
                    response = requests.get(url, params=params, timeout=5)
                    if response.status_code == 200:
                        data = response.json()
                        if data.get("status") == "OK" and data.get("results"):
                            location = data["results"][0]["geometry"]["location"]
                            self.latitude = location["lat"]
                            self.longitude = location["lng"]
                except Exception:
                    # Fallback silently or log in a production app
                    pass
        super().save(*args, **kwargs)

from django.contrib import admin
from .models import Doctor

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialty', 'clinic_name', 'rating', 'latitude', 'longitude')
    list_filter = ('specialty', 'rating')
    search_fields = ('name', 'clinic_name', 'address', 'email')
    fieldsets = (
        ('General Information', {
            'fields': ('name', 'specialty', 'clinic_name', 'rating')
        }),
        ('Contact Information', {
            'fields': ('phone_number', 'email', 'website')
        }),
        ('Location & Coordinates', {
            'fields': ('address', 'latitude', 'longitude'),
            'description': 'Leave latitude and longitude empty to auto-geocode if a Google Maps API Key is configured in settings.'
        }),
    )

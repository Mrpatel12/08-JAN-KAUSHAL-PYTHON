from django.contrib import admin
from .models import Category, Accommodation, Flight, TravelPackage

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon')

@admin.register(Accommodation)
class AccommodationAdmin(admin.ModelAdmin):
    list_display = ('name', 'accommodation_type', 'location', 'price_per_night', 'rating')
    list_filter = ('accommodation_type', 'location')
    search_fields = ('name', 'location')

@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ('airline', 'flight_number', 'origin', 'destination', 'departure_time', 'price')
    list_filter = ('airline', 'origin', 'destination')
    search_fields = ('airline', 'flight_number')

@admin.register(TravelPackage)
class TravelPackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'destinations', 'duration_days', 'price', 'is_featured')
    list_filter = ('is_featured',)
    search_fields = ('name', 'destinations')

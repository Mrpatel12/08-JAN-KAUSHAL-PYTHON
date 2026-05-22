import json
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q
from django.conf import settings
from .models import Doctor

def index_view(request):
    # Retrieve default specialties for filters
    specialties = [choice[0] for choice in Doctor.SPECIALTY_CHOICES]
    
    # We pass the backend Google Maps API Key to the template.
    # If it's not set, the frontend will show a fallback settings dialog.
    context = {
        'google_maps_api_key': getattr(settings, 'GOOGLE_MAPS_API_KEY', ''),
        'specialties': specialties,
    }
    return render(request, 'map_app/index.html', context)

def api_doctors_list(request):
    specialty = request.GET.get('specialty', '')
    query = request.GET.get('q', '')
    
    doctors = Doctor.objects.all()
    
    if specialty:
        doctors = doctors.filter(specialty__iexact=specialty)
        
    if query:
        doctors = doctors.filter(
            Q(name__icontains=query) |
            Q(clinic_name__icontains=query) |
            Q(address__icontains=query)
        )
        
    data = []
    for d in doctors:
        data.append({
            'id': d.id,
            'name': d.name,
            'specialty': d.specialty,
            'clinic_name': d.clinic_name,
            'address': d.address,
            'latitude': float(d.latitude) if d.latitude is not None else None,
            'longitude': float(d.longitude) if d.longitude is not None else None,
            'phone_number': d.phone_number,
            'email': d.email,
            'rating': float(d.rating),
            'website': d.website,
        })
        
    return JsonResponse(data, safe=False)

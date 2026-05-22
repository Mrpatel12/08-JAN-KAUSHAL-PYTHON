from django.shortcuts import render, get_object_or_404
from .models import Accommodation, Flight, TravelPackage
from django.http import HttpResponseRedirect
from django.urls import reverse

COMMON_CITIES = [
    "Agartala", "Agra", "Ahmedabad", "Aizawl", "Amritsar", "Aurangabad", "Ayodhya", "Bagdogra", 
    "Bareilly", "Belagavi", "Bengaluru", "Bhavnagar", "Bhopal", "Bhubaneswar", "Bhuj", "Bikaner", 
    "Chandigarh", "Chennai", "Coimbatore", "Darbhanga", "Dehradun", "Delhi", "Deoghar", 
    "Dharamshala", "Dibrugarh", "Dimapur", "Durgapur", "Gaya", "Goa", "Gorakhpur", "Guwahati", 
    "Gwalior", "Hubli", "Hyderabad", "Imphal", "Indore", "Itanagar", "Jabalpur", "Jaipur", 
    "Jammu", "Jamnagar", "Jodhpur", "Jorhat", "Kadapa", "Kanpur", "Khajuraho", "Kochi", 
    "Kolkata", "Kozhikode", "Kullu", "Kurnool", "Leh", "Lucknow", "Madurai", "Mangaluru", 
    "Mumbai", "Mysuru", "Nagpur", "Nanded", "Nashik", "Pantnagar", "Patna", "Port Blair", 
    "Prayagraj", "Pune", "Raipur", "Rajahmundry", "Rajkot", "Ranchi", "Shillong", "Shimla", 
    "Silchar", "Srinagar", "Surat", "Thiruvananthapuram", "Tiruchirappalli", "Tirupati", 
    "Tuticorin", "Udaipur", "Vadodara", "Varanasi", "Vijayawada", "Visakhapatnam",
    "Dubai", "London", "New York", "Singapore", "Paris", "Tokyo", "Bangkok"
]

def services_list(request):
    accommodations = Accommodation.objects.all()
    flights = Flight.objects.all().order_by('departure_time')
    packages = TravelPackage.objects.all()
    
    # Get distinct locations from DB
    db_origins = list(Flight.objects.values_list('origin', flat=True).distinct())
    db_destinations = list(Flight.objects.values_list('destination', flat=True).distinct())
    
    # Combine with common cities and remove duplicates
    all_cities = sorted(list(set(db_origins + db_destinations + COMMON_CITIES)))
    
    # Handle search filtering
    search_origin = request.GET.get('origin', '')
    search_dest = request.GET.get('destination', '')
    
    if search_origin:
        flights = flights.filter(origin__icontains=search_origin)
    if search_dest:
        flights = flights.filter(destination__icontains=search_dest)
    
    context = {
        'accommodations': accommodations,
        'flights': flights,
        'packages': packages,
        'all_cities': all_cities,
        'search_origin': search_origin,
        'search_dest': search_dest,
    }
    return render(request, 'services/list.html', context)

def flights_list(request):
    flights = Flight.objects.all().order_by('departure_time')
    flight_type = request.GET.get('type')
    if flight_type == 'international':
        flights = flights.filter(is_international=True)
    elif flight_type == 'national':
        flights = flights.filter(is_international=False)
        
    search_origin = request.GET.get('origin', '')
    search_dest = request.GET.get('destination', '')
    if search_origin:
        flights = flights.filter(origin__icontains=search_origin)
    if search_dest:
        flights = flights.filter(destination__icontains=search_dest)
        
    context = {'flights': flights, 'search_origin': search_origin, 'search_dest': search_dest, 'COMMON_CITIES': COMMON_CITIES}
    return render(request, 'services/flights.html', context)

def accommodations_list(request):
    accommodations = Accommodation.objects.all()
    acc_type = request.GET.get('type')
    if acc_type:
        accommodations = accommodations.filter(accommodation_type=acc_type.upper())
    context = {'accommodations': accommodations}
    return render(request, 'services/accommodations.html', context)

def packages_list(request):
    packages = TravelPackage.objects.all()
    context = {'packages': packages}
    return render(request, 'services/packages.html', context)


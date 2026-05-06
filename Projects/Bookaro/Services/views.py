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

def flight_payment(request):
    """Simple payment page for selected flight"""
    flight_id = request.GET.get('flight_id') or request.POST.get('flight_id')
    flight = get_object_or_404(Flight, id=flight_id)
    payment_methods = [
        {'name': 'UPI', 'icon': 'fa-solid fa-mobile-alt'},
        {'name': 'Credit Card', 'icon': 'fa-solid fa-credit-card'},
        {'name': 'Debit Card', 'icon': 'fa-solid fa-credit-card'},
        {'name': 'Net Banking', 'icon': 'fa-solid fa-university'},
        {'name': 'Wallet', 'icon': 'fa-solid fa-wallet'},
    ]
    if request.method == 'POST':
        # In a real app you would process payment here.
        # For now just redirect to success page or back to services.
        return HttpResponseRedirect(reverse('services_list'))
    return render(request, 'services/payment.html', {'flight': flight, 'payment_methods': payment_methods})



from django.shortcuts import render
import requests
from datetime import datetime

def index(request):
    weather_data = {}
    error_message = ""
    
    if request.method == 'POST':
        city = request.POST.get('city', '').strip()
        if city:
            api_key = "30791ae69e280b62dcde5ea95db232c1"
            # Using metric units for Celsius
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}"
            
            try:
                response = requests.get(url)
                data = response.json()
                
                if response.status_code == 200:
                    weather_data = {
                        'city': data['name'],
                        'temperature': data['main']['temp'],
                        'feels_like': data['main']['feels_like'],
                        'description': data['weather'][0]['description'],
                        'icon': data['weather'][0]['icon'],
                        'humidity': data['main']['humidity'],
                        'wind_speed': data['wind']['speed'],
                        'pressure': data['main']['pressure'],
                        'visibility': data.get('visibility', 0) / 1000, # Convert to km
                        'country': data['sys']['country'],
                        'sunrise': datetime.fromtimestamp(data['sys']['sunrise']).strftime('%I:%M %p'),
                        'sunset': datetime.fromtimestamp(data['sys']['sunset']).strftime('%I:%M %p'),
                        'timestamp': datetime.now().strftime('%A, %b %d, %Y'),
                        'main_condition': data['weather'][0]['main'].lower()
                    }
                else:
                    error_message = data.get('message', 'City not found. Please try again.').capitalize()
            except Exception as e:
                error_message = "An error occurred while fetching the weather data."
        else:
            error_message = "Please enter a city name."

    return render(request, 'index.html', {'weather': weather_data, 'error': error_message})

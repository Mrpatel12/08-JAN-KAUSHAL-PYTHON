import requests
from django.shortcuts import render
from .serializers import ProductSerializer

def index(request):
    # Fetch data from external API
    url = "https://fakestoreapi.com/products"
    response = requests.get(url)
    
    if response.status_code == 200:
        raw_data = response.json()
        
        # Deserialization process:
        # We pass the raw JSON data to the serializer with many=True
        serializer = ProductSerializer(data=raw_data, many=True)
        
        if serializer.is_valid():
            # serializer.validated_data is the 'deserialized' Python object
            products = serializer.validated_data
        else:
            # Handle validation errors
            products = []
            print(serializer.errors)
    else:
        products = []

    return render(request, 'index.html', {'products': products})

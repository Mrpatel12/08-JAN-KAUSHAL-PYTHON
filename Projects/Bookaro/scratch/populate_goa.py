import os
import django
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Bookaro.settings')
django.setup()

from Services.models import Accommodation, TravelPackage, Category

def populate():
    print("Populating Goa data...")
    
    # Ensure a Category exists
    luxury_cat, _ = Category.objects.get_or_create(name="Luxury Stays", icon="hotel")
    beach_cat, _ = Category.objects.get_or_create(name="Beach Escapes", icon="umbrella-beach")

    # Goa Accommodations
    accommodations = [
        {
            "name": "Taj Exotica Resort & Spa",
            "accommodation_type": "HOTEL",
            "location": "Benaulim, Goa",
            "price_per_night": Decimal('18500.00'),
            "description": "A Mediterranean-style resort overlooking the Arabian Sea, featuring lush gardens and world-class spa facilities.",
            "image_url": "https://images.unsplash.com/photo-1540541338287-41700207dee6?q=80&w=2670",
            "rating": 4.9
        },
        {
            "name": "The Leela Goa",
            "accommodation_type": "HOTEL",
            "location": "Cavelossim, Goa",
            "price_per_night": Decimal('22000.00'),
            "description": "Experience the ultimate luxury with riverside views and beach access, inspired by the Vijayanagara Empire architecture.",
            "image_url": "https://images.unsplash.com/photo-1571896349842-33c89424de2d?q=80&w=2670",
            "rating": 5.0
        },
        {
            "name": "W Goa",
            "accommodation_type": "HOTEL",
            "location": "Vagator, Goa",
            "price_per_night": Decimal('15000.00'),
            "description": "A vibrant and trendy resort near Vagator Beach, perfect for those seeking nightlife and modern luxury.",
            "image_url": "https://images.unsplash.com/photo-1582719508461-905c673771fd?q=80&w=2650",
            "rating": 4.7
        },
        {
            "name": "Private Infinity Villa",
            "accommodation_type": "VILLA",
            "location": "Anjuna, Goa",
            "price_per_night": Decimal('35000.00'),
            "description": "An exclusive 4-bedroom villa with a private infinity pool overlooking the cliffs of Anjuna.",
            "image_url": "https://images.unsplash.com/photo-1613490493576-7fde63acd811?q=80&w=2671",
            "rating": 4.9
        }
    ]

    for acc_data in accommodations:
        acc, created = Accommodation.objects.get_or_create(
            name=acc_data["name"],
            defaults=acc_data
        )
        if created:
            print(f"Created accommodation: {acc.name}")

    # Goa Travel Packages
    packages = [
        {
            "name": "Goa Beach Bliss Honeymoon",
            "destinations": "South Goa, Benaulim, Palolem",
            "duration_days": 5,
            "price": Decimal('45000.00'),
            "description": "A romantic 5-day getaway focusing on the serene beaches of South Goa, including candlelit dinners and spa sessions.",
            "image_url": "https://images.unsplash.com/photo-1512100356956-c1227c3317bb?q=80&w=2670",
            "is_featured": True
        },
        {
            "name": "Goa Adventure Explorer",
            "destinations": "North Goa, Dudhsagar Falls, Old Goa",
            "duration_days": 4,
            "price": Decimal('28500.00'),
            "description": "Experience the thrill of Goa with scuba diving, waterfall trekking, and heritage tours of Old Goa.",
            "image_url": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?q=80&w=2673",
            "is_featured": True
        },
        {
            "name": "Luxury Goa Escape",
            "destinations": "Private Island, Goa",
            "duration_days": 3,
            "price": Decimal('85000.00'),
            "description": "Ultra-premium 3-day stay at a private island resort with helicopter transfers and personal butler service.",
            "image_url": "https://images.unsplash.com/photo-1499793983690-e29da59ef1c2?q=80&w=2670",
            "is_featured": True
        }
    ]

    for pkg_data in packages:
        pkg, created = TravelPackage.objects.get_or_create(
            name=pkg_data["name"],
            defaults=pkg_data
        )
        if created:
            print(f"Created package: {pkg.name}")

    print("Finished populating Goa data!")

if __name__ == "__main__":
    populate()

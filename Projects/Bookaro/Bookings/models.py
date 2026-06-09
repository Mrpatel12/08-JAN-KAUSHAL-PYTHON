from django.db import models
from django.contrib.auth.models import User
from Services.models import Accommodation, Flight, TravelPackage

class Booking(models.Model):
    SERVICE_CHOICES = [
        ('ACCOMMODATION', 'Accommodation'),
        ('FLIGHT', 'Flight'),
        ('PACKAGE', 'Travel Package'),
    ]
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    service_type = models.CharField(max_length=20, choices=SERVICE_CHOICES)
    
    accommodation = models.ForeignKey(Accommodation, on_delete=models.SET_NULL, null=True, blank=True)
    flight = models.ForeignKey(Flight, on_delete=models.SET_NULL, null=True, blank=True)
    package = models.ForeignKey(TravelPackage, on_delete=models.SET_NULL, null=True, blank=True)
    
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    selected_seat = models.CharField(max_length=10, blank=True, null=True, help_text="Selected seat for flight (e.g., 12A)")
    room_type = models.CharField(max_length=50, blank=True, null=True, help_text="Room preferences or type")

    def __str__(self):
        return f"Booking #{self.id} by {self.user.username} - {self.status}"

class Payment(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='payment')
    razorpay_order_id = models.CharField(max_length=100, unique=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=255, blank=True, null=True)
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    is_successful = models.BooleanField(default=False)

    def __str__(self):
        return f"Payment for Booking #{self.booking.id}"

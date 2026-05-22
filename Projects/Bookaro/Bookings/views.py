import razorpay
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from .models import Booking, Payment
from Services.models import Flight, Accommodation, TravelPackage

razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

@login_required
def checkout_view(request):
    if request.method == 'POST':
        service_type = request.POST.get('service_type')
        service_id = request.POST.get('service_id')
        
        booking = Booking(user=request.user, service_type=service_type, status='PENDING')
        amount = 0
        
        if service_type == 'FLIGHT':
            flight = get_object_or_404(Flight, id=service_id)
            booking.flight = flight
            amount = flight.price
        elif service_type == 'ACCOMMODATION':
            acc = get_object_or_404(Accommodation, id=service_id)
            booking.accommodation = acc
            amount = acc.price_per_night
        elif service_type == 'PACKAGE':
            pkg = get_object_or_404(TravelPackage, id=service_id)
            booking.package = pkg
            amount = pkg.price
            
        booking.total_amount = amount
        booking.save()
        
        currency = 'INR'
        amount_in_paise = int(amount * 100)
        razorpay_order = razorpay_client.order.create(dict(amount=amount_in_paise, currency=currency, payment_capture='0'))
        
        payment = Payment.objects.create(
            booking=booking,
            razorpay_order_id=razorpay_order['id'],
            amount_paid=amount
        )
        
        context = {
            'booking': booking,
            'payment': payment,
            'razorpay_order_id': razorpay_order['id'],
            'razorpay_merchant_key': settings.RAZORPAY_KEY_ID,
            'amount_in_paise': amount_in_paise,
            'currency': currency,
        }
        return render(request, 'bookings/checkout.html', context)
    return redirect('home')

@csrf_exempt
def payment_success_view(request):
    if request.method == "POST":
        razorpay_payment_id = request.POST.get('razorpay_payment_id', '')
        razorpay_order_id = request.POST.get('razorpay_order_id', '')
        razorpay_signature = request.POST.get('razorpay_signature', '')
        
        payment = get_object_or_404(Payment, razorpay_order_id=razorpay_order_id)
        
        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        }
        
        try:
            razorpay_client.utility.verify_payment_signature(params_dict)
            payment.razorpay_payment_id = razorpay_payment_id
            payment.razorpay_signature = razorpay_signature
            payment.is_successful = True
            payment.save()
            
            booking = payment.booking
            booking.status = 'CONFIRMED'
            booking.save()
            
            return render(request, 'bookings/success.html', {'booking': booking})
        except razorpay.errors.SignatureVerificationError:
            return render(request, 'bookings/failed.html', {'payment': payment})
    return HttpResponseBadRequest()

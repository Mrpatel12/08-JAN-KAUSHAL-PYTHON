from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from Bookings.models import Booking
from django.db.models import Sum

@login_required
def dashboard_view(request):
    # Fetch all bookings for the current user
    user_bookings = Booking.objects.filter(user=request.user).order_by('-booking_date')
    
    # Calculate premium statistics
    total_bookings = user_bookings.count()
    active_bookings = user_bookings.filter(status='CONFIRMED').count()
    pending_bookings = user_bookings.filter(status='PENDING').count()
    cancelled_bookings = user_bookings.filter(status='CANCELLED').count()
    
    # Spend breakdown
    total_spent = user_bookings.filter(status='CONFIRMED').aggregate(Sum('total_amount'))['total_amount__sum'] or 0.00
    
    # Reward Points (Simulated: 10 points for every 1000 INR spent)
    reward_points = int(total_spent / 100)
    
    # Profile completeness score
    profile_score = 40
    if request.user.first_name: profile_score += 20
    if request.user.last_name: profile_score += 20
    if hasattr(request.user, 'profile') and request.user.profile.avatar: profile_score += 20
    
    context = {
        'bookings': user_bookings,
        'stats': {
            'total': total_bookings,
            'active': active_bookings,
            'pending': pending_bookings,
            'cancelled': cancelled_bookings,
            'spent': total_spent,
            'points': reward_points,
            'profile_score': profile_score
        }
    }
    return render(request, 'dashboard/index.html', context)

@login_required
def cancel_booking_view(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    if booking.status != 'CANCELLED':
        booking.status = 'CANCELLED'
        booking.save()
        messages.success(request, f"Booking #{booking.id} has been successfully cancelled.")
    else:
        messages.warning(request, f"Booking #{booking.id} is already cancelled.")
    return redirect('dashboard')

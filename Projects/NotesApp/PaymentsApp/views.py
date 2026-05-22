import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Payment
from django.contrib.auth import get_user_model

User = get_user_model()
stripe.api_key = settings.STRIPE_SECRET_KEY

def pricing_page(request):
    return render(request, 'PaymentsApp/pricing.html', {
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY
    })

@login_required
def create_checkout_session(request):
    # For simplicity, we use a fixed price for Premium
    # In a real app, you might have multiple prices or products
    try:
        checkout_session = stripe.checkout.Session.create(
            customer_email=request.user.email,
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': 'NotesApp Premium Plan',
                            'description': 'Unlock unlimited notes and advanced features',
                        },
                        'unit_amount': 999, # $9.99
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=settings.SITE_URL + '/payments/success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=settings.SITE_URL + '/payments/cancel',
        )
        
        # Save payment record
        Payment.objects.create(
            user=request.user,
            stripe_checkout_id=checkout_session.id,
            amount=9.99,
            status='pending'
        )
        
        return redirect(checkout_session.url, code=303)
    except Exception as e:
        return JsonResponse({'error': str(e)})

@login_required
def payment_success(request):
    session_id = request.GET.get('session_id')
    if session_id:
        try:
            session = stripe.checkout.Session.retrieve(session_id)
            payment = Payment.objects.get(stripe_checkout_id=session_id)
            if session.payment_status == 'paid':
                payment.status = 'completed'
                payment.save()
                
                # Update user premium status
                user = request.user
                user.is_premium = True
                user.save()
                
            return render(request, 'PaymentsApp/success.html')
        except Exception:
            return redirect('pricing')
    return redirect('pricing')

@login_required
def payment_cancel(request):
    return render(request, 'PaymentsApp/cancel.html')

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        
        # Get user email or other identifiers
        customer_email = session.get('customer_email')
        if customer_email:
            try:
                user = User.objects.get(email=customer_email)
                user.is_premium = True
                user.save()
                
                # Update payment record if it exists
                payment = Payment.objects.filter(stripe_checkout_id=session.get('id')).first()
                if payment:
                    payment.status = 'completed'
                    payment.save()
            except User.DoesNotExist:
                pass

    return HttpResponse(status=200)

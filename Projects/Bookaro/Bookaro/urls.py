"""
URL configuration for Bookaro project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from Accounts import views as accounts_views
from Services import views as services_views
from Bookings import views as bookings_views
from Dashboard import views as dashboard_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', accounts_views.home, name='home'),
    path('about/', accounts_views.about_view, name='about'),
    path('services/', services_views.services_list, name='services_list'),
    path('services/flights/', services_views.flights_list, name='flights_list'),
    path('services/accommodations/', services_views.accommodations_list, name='accommodations_list'),
    path('services/packages/', services_views.packages_list, name='packages_list'),
    path('checkout/', bookings_views.checkout_view, name='checkout'),
    path('payment/success/', bookings_views.payment_success_view, name='payment_success'),
    path('signup/', accounts_views.signup_view, name='signup'),
    path('verify-otp/', accounts_views.verify_otp_view, name='verify_otp'),
    path('resend-otp/', accounts_views.resend_otp_view, name='resend_otp'),
    path('profile/edit/', accounts_views.edit_profile_view, name='edit_profile'),
    path('login/', accounts_views.login_view, name='login'),
    path('logout/', accounts_views.logout_view, name='logout'),
    path('contact/', accounts_views.contact_view, name='contact'),
    path('dashboard/', dashboard_views.dashboard_view, name='dashboard'),
    path('bookings/cancel/<int:booking_id>/', dashboard_views.cancel_booking_view, name='cancel_booking'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

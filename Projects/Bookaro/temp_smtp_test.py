import os, sys, traceback
from pathlib import Path

sys.path.insert(0, os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Bookaro.settings')
import django

django.setup()

from django.conf import settings
from django.contrib.auth.models import User
from Accounts.models import EmailOTP
from django.core.mail import send_mail

print('Using settings:')
print('DEBUG =', settings.DEBUG)
print('EMAIL_BACKEND =', getattr(settings, 'EMAIL_BACKEND', None))
print('EMAIL_HOST =', getattr(settings, 'EMAIL_HOST', None))
print('EMAIL_PORT =', getattr(settings, 'EMAIL_PORT', None))
print('EMAIL_HOST_USER =', getattr(settings, 'EMAIL_HOST_USER', None))

# Override backend to SMTP for this test regardless of DEBUG
settings.EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
settings.EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
settings.EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
settings.EMAIL_USE_TLS = True
settings.EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
settings.EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
settings.DEFAULT_FROM_EMAIL = settings.EMAIL_HOST_USER

if not settings.EMAIL_HOST_USER or not settings.EMAIL_HOST_PASSWORD:
    print('\nERROR: EMAIL_HOST_USER or EMAIL_HOST_PASSWORD not set in environment.')
    print('Set them in your OS or create a .env file and export them before running this test.')
    sys.exit(1)

# Create/get a test user with the recipient email
recipient = settings.EMAIL_HOST_USER
user, created = User.objects.get_or_create(username='smtp_test_user', defaults={'email': recipient})
if created:
    user.set_password('testpass')
    user.save()

import random
otp = f"{random.randint(100000, 999999)}"
EmailOTP.objects.update_or_create(user=user, defaults={'otp': otp})
print('\nSaved OTP in DB:', otp)

try:
    send_mail(
        'SMTP Test OTP',
        f'Your SMTP test OTP is: {otp}',
        settings.DEFAULT_FROM_EMAIL,
        [recipient],
        fail_silently=False,
    )
    print('\nSMTP send_mail completed successfully - check recipient inbox (Gmail).')
except Exception:
    print('\nSMTP send_mail raised an exception:')
    traceback.print_exc()

import os, sys, traceback
from pathlib import Path

sys.path.insert(0, os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Bookaro.settings')
import django
django.setup()

from django.contrib.auth.models import User
from Accounts.models import EmailOTP
from django.core.mail import send_mail
from django.conf import settings

email = settings.EMAIL_HOST_USER
username = 'test_otp_user'

try:
    user, created = User.objects.get_or_create(username=username, defaults={'email': email})
    if created:
        user.set_password('TestPassword123')
        user.is_active = False
        user.save()
        print(f'Created test user: {user.username} ({user.email})')
    else:
        print(f'Using existing user: {user.username} ({user.email})')

    import random
    otp = f"{random.randint(100000, 999999)}"
    EmailOTP.objects.update_or_create(user=user, defaults={'otp': otp})
    print('Saved OTP in DB:', otp)

    try:
        send_mail(
            'Test OTP',
            f'Your test OTP is: {otp}',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        print('send_mail completed successfully (console backend should have printed OTP).')
    except Exception as e:
        print('Error during send_mail:')
        traceback.print_exc()

except Exception as e:
    print('Script failed:')
    traceback.print_exc()

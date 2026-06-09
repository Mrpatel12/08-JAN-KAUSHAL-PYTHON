import os, sys
from pathlib import Path

sys.path.insert(0, os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Bookaro.settings')
import django
django.setup()

from django.conf import settings

password = settings.EMAIL_HOST_PASSWORD
print('Password from settings:', repr(password))
print('Password length:', len(password))
print('Password without spaces:', repr(password.replace(' ', '')))
print('Password without spaces length:', len(password.replace(' ', '')))

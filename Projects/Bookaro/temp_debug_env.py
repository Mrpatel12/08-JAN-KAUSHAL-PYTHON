import os, sys
from pathlib import Path

sys.path.insert(0, os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Bookaro.settings')

# Show what's in environment BEFORE Django loads settings
print('=== Environment Variables (BEFORE Django) ===')
print('EMAIL_HOST_USER from OS:', os.environ.get('EMAIL_HOST_USER', '[NOT SET]'))
print('EMAIL_HOST_PASSWORD from OS:', '***' if os.environ.get('EMAIL_HOST_PASSWORD') else '[NOT SET]')

# Show .env file location and contents
env_file = Path('.env')
print('\n=== .env File ===')
print('.env exists at', env_file.absolute(), ':', env_file.exists())
if env_file.exists():
    print('.env contents:')
    print(env_file.read_text(encoding='utf-8'))

# Now load Django
import django
django.setup()

from django.conf import settings

# Show what Django loaded
print('\n=== Django Settings (AFTER settings.py loaded) ===')
print('EMAIL_HOST_USER:', settings.EMAIL_HOST_USER)
print('EMAIL_HOST_PASSWORD:', '***' if settings.EMAIL_HOST_PASSWORD else '[NOT SET]')
print('EMAIL_HOST:', settings.EMAIL_HOST)
print('EMAIL_PORT:', settings.EMAIL_PORT)
print('EMAIL_USE_TLS:', settings.EMAIL_USE_TLS)
print('EMAIL_BACKEND:', settings.EMAIL_BACKEND)

print('\n=== Summary ===')
if settings.EMAIL_HOST_USER and 'your' in settings.EMAIL_HOST_USER.lower():
    print('ERROR: EMAIL_HOST_USER is a placeholder. .env not loaded correctly.')
elif settings.EMAIL_HOST_USER and settings.EMAIL_HOST_PASSWORD:
    print('OK: Credentials appear to be set. Email:', settings.EMAIL_HOST_USER)
else:
    print('ERROR: Credentials are missing or empty.')

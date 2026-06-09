import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Farmledger.settings')
django.setup()

from django.apps import apps
for a in apps.get_app_configs():
    print(a.name)

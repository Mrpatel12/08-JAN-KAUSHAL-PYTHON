from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from .models import Crop
from apps.farms.models import Farm

User = get_user_model()


class CropAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='user@example.com', password='password123')  # nosec: B106
        self.farm = Farm.objects.create(owner=self.user, name='User Farm', slug='user-farm')

    def test_create_crop(self):
        self.client.force_authenticate(self.user)
        payload = {'farm_id': str(self.farm.id), 'name': 'Maize'}
        resp = self.client.post('/api/v1/crops/', payload, format='json')
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.json()['name'], 'Maize')

    def test_list_crops(self):
        Crop.objects.create(farm=self.farm, name='Crop1')
        Crop.objects.create(farm=self.farm, name='Crop2')
        self.client.force_authenticate(self.user)
        resp = self.client.get('/api/v1/crops/')
        self.assertEqual(resp.status_code, 200)
        body = resp.json()
        items = body.get('results', body)
        self.assertGreaterEqual(len(items), 2)

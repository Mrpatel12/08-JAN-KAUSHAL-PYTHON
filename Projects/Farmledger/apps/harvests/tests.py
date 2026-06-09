from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from apps.farms.models import Farm
from .models import Harvest

User = get_user_model()


class HarvestAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='h@example.com', password='password')  # nosec: B106
        self.farm = Farm.objects.create(owner=self.user, name='F', slug='f')

    def test_create_harvest(self):
        self.client.force_authenticate(self.user)
        payload = {'farm_id': str(self.farm.id), 'quantity': '100.5', 'unit': 'kg'}
        resp = self.client.post('/api/v1/harvests/', payload, format='json')
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.json()['unit'], 'kg')

    def test_list_harvests(self):
        Harvest.objects.create(farm=self.farm, quantity='10')
        Harvest.objects.create(farm=self.farm, quantity='20')
        self.client.force_authenticate(self.user)
        resp = self.client.get('/api/v1/harvests/')
        self.assertEqual(resp.status_code, 200)
        body = resp.json()
        items = body.get('results', body)
        self.assertGreaterEqual(len(items), 2)

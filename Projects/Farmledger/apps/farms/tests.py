from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from .models import Farm
from django.urls import reverse


User = get_user_model()


class FarmAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='owner@example.com', password='password123')  # nosec: B106
        self.other = User.objects.create_user(email='other@example.com', password='password123')  # nosec: B106
        self.farm1 = Farm.objects.create(owner=self.user, name='Farm A', slug='farm-a')
        self.farm2 = Farm.objects.create(owner=self.user, name='Farm B', slug='farm-b')
        self.other_farm = Farm.objects.create(owner=self.other, name='Other Farm', slug='other-farm')

    def test_list_shows_only_owner_farms(self):
        self.client.force_authenticate(self.user)
        resp = self.client.get('/api/v1/farms/')
        self.assertEqual(resp.status_code, 200)
        body = resp.json()
        items = body.get('results', body)
        ids = {item['id'] for item in items}
        self.assertIn(str(self.farm1.id), ids)
        self.assertIn(str(self.farm2.id), ids)
        self.assertNotIn(str(self.other_farm.id), ids)

    def test_create_farm_sets_owner(self):
        self.client.force_authenticate(self.user)
        payload = {'name': 'New Farm', 'slug': 'new-farm'}
        resp = self.client.post('/api/v1/farms/', payload, format='json')
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.json()['owner'], str(self.user.id))

    def test_retrieve_farm(self):
        self.client.force_authenticate(self.user)
        resp = self.client.get(f'/api/v1/farms/{self.farm1.id}/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['id'], str(self.farm1.id))

    def test_update_farm(self):
        self.client.force_authenticate(self.user)
        resp = self.client.patch(f'/api/v1/farms/{self.farm1.id}/', {'name': 'Updated'}, format='json')
        self.assertEqual(resp.status_code, 200)
        self.farm1.refresh_from_db()
        self.assertEqual(self.farm1.name, 'Updated')

    def test_delete_farm(self):
        self.client.force_authenticate(self.user)
        resp = self.client.delete(f'/api/v1/farms/{self.farm2.id}/')
        self.assertIn(resp.status_code, (204, 200))
        self.assertFalse(Farm.objects.filter(id=self.farm2.id).exists())

    def test_stats_action(self):
        self.client.force_authenticate(self.user)
        resp = self.client.get(f'/api/v1/farms/{self.farm1.id}/stats/')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('total_crops', resp.json())

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from apps.farms.models import Farm
from .models import Expense

User = get_user_model()


class ExpenseAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='u@example.com', password='password')  # nosec: B106
        self.farm = Farm.objects.create(owner=self.user, name='F', slug='f')

    def test_create_expense(self):
        self.client.force_authenticate(self.user)
        payload = {'farm_id': str(self.farm.id), 'amount': '123.45', 'category': 'seed'}
        resp = self.client.post('/api/v1/expenses/', payload, format='json')
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.json()['category'], 'seed')

    def test_list_expenses(self):
        Expense.objects.create(farm=self.farm, amount='10.00')
        Expense.objects.create(farm=self.farm, amount='20.00')
        self.client.force_authenticate(self.user)
        resp = self.client.get('/api/v1/expenses/')
        self.assertEqual(resp.status_code, 200)
        body = resp.json()
        items = body.get('results', body)
        self.assertGreaterEqual(len(items), 2)

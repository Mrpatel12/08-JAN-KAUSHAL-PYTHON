from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import UserProfile

class RegistrationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('accounts:register')
        self.success_url = reverse('accounts:success')

    def test_register_page_loads(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')

    def test_success_page_loads(self):
        response = self.client.get(self.success_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/success.html')

    def test_user_registration_creates_user_and_profile(self):
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'phone_number': '9876543210',
            'password1': 'StrongPass!123',
            'password2': 'StrongPass!123',
        }
        response = self.client.post(self.register_url, data)
        # Should redirect to success page
        self.assertRedirects(response, self.success_url)
        
        # User and Profile should exist in the database
        user = User.objects.filter(username='testuser').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.profile.phone_number, '9876543210')
        
        # Session should contain the registered phone number
        self.assertEqual(self.client.session.get('registered_phone'), '9876543210')

    def test_duplicate_phone_number_rejected(self):
        # Create an existing user and profile
        user = User.objects.create_user('existinguser', 'existing@example.com', 'pass123')
        UserProfile.objects.create(user=user, phone_number='9876543210')

        # Try to register another user with the same phone number
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'phone_number': '9876543210',
            'password1': 'StrongPass!123',
            'password2': 'StrongPass!123',
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='newuser').exists())
        self.assertIn('An account with this phone number already exists.', response.content.decode())

    def test_invalid_phone_number_rejected(self):
        # Test non-numeric phone number
        data = {
            'username': 'newuser2',
            'email': 'new2@example.com',
            'phone_number': '98765abcd0',
            'password1': 'StrongPass!123',
            'password2': 'StrongPass!123',
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='newuser2').exists())

        # Test short phone number
        data['phone_number'] = '12345'
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='newuser2').exists())

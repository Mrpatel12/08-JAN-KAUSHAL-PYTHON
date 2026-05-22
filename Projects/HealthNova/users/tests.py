from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken

User = get_user_model()

class UserAuthTests(APITestCase):
    def setUp(self):
        self.register_url = reverse('auth_register')
        self.login_url = reverse('token_obtain_pair')
        self.profile_url = reverse('auth_profile')

        self.user_data = {
            'username': 'patient_test',
            'password': 'SecurePassword123!',
            'email': 'patient@test.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'phone_number': '1234567890'
        }

    def test_registration_success(self):
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], 'patient_test')
        self.assertNotIn('password', response.data)

        # Verify default role is PATIENT
        user = User.objects.get(username='patient_test')
        self.assertEqual(user.role, User.Role.PATIENT)

    def test_registration_duplicate_email(self):
        # Create initial user
        self.client.post(self.register_url, self.user_data)
        # Attempt to register again with same email but different username
        data = self.user_data.copy()
        data['username'] = 'patient_test_2'
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    def test_login_success_and_jwt_payload(self):
        # Register user
        self.client.post(self.register_url, self.user_data)

        # Login
        login_data = {
            'username': 'patient_test',
            'password': 'SecurePassword123!'
        }
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

        # Verify custom response structure
        self.assertEqual(response.data['user']['username'], 'patient_test')
        self.assertEqual(response.data['user']['role'], 'PATIENT')

        # Decode token and verify custom claims
        token = AccessToken(response.data['access'])
        self.assertEqual(token['role'], 'PATIENT')
        self.assertEqual(token['username'], 'patient_test')
        self.assertEqual(token['email'], 'patient@test.com')

    def test_profile_access_restricted(self):
        # Access profile without token
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_profile_access_success(self):
        # Register and login user
        self.client.post(self.register_url, self.user_data)
        login_data = {
            'username': 'patient_test',
            'password': 'SecurePassword123!'
        }
        response = self.client.post(self.login_url, login_data)
        token = response.data['access']

        # Authorize client
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'patient_test')

        # Update profile
        update_data = {'first_name': 'Johnny'}
        response = self.client.patch(self.profile_url, update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'Johnny')

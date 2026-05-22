from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from doctors.models import DoctorProfile

User = get_user_model()

class DoctorProfileTests(APITestCase):
    def setUp(self):
        # Create users
        self.admin = User.objects.create_user(
            username='admin_user', password='password', email='admin@test.com', role=User.Role.ADMIN
        )
        self.doctor_user1 = User.objects.create_user(
            username='doc_user1', password='password', email='doc1@test.com', role=User.Role.DOCTOR
        )
        self.doctor_user2 = User.objects.create_user(
            username='doc_user2', password='password', email='doc2@test.com', role=User.Role.DOCTOR
        )
        self.patient = User.objects.create_user(
            username='patient_user', password='password', email='patient@test.com', role=User.Role.PATIENT
        )

        self.list_url = reverse('doctor-list')

        # Create doctor profile for doc_user1
        self.profile1 = DoctorProfile.objects.create(
            user=self.doctor_user1,
            specialization='Cardiology',
            experience_years=10,
            clinic_name='Heart Care Clinic',
            bio='Cardiology expert.',
            consultation_fee=150.00
        )

    def test_list_and_retrieve_public(self):
        # Public listing (no authentication)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        # Public detail
        detail_url = reverse('doctor-detail', args=[self.profile1.id])
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['specialization'], 'Cardiology')

    def test_create_doctor_profile_restricted(self):
        # Authenticate as patient
        self.client.force_authenticate(user=self.patient)
        data = {
            'user': self.doctor_user2.id,
            'specialization': 'Dermatology',
            'experience_years': 5,
            'clinic_name': 'Skin Clinic',
            'consultation_fee': 100.00
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Authenticate as Admin
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(DoctorProfile.objects.filter(user=self.doctor_user2).count(), 1)

    def test_update_doctor_profile_rbac(self):
        detail_url = reverse('doctor-detail', args=[self.profile1.id])
        update_data = {'specialization': 'Pediatrics'}

        # Non-owner Doctor attempts update
        self.client.force_authenticate(user=self.doctor_user2)
        response = self.client.patch(detail_url, update_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Owner Doctor attempts update
        self.client.force_authenticate(user=self.doctor_user1)
        response = self.client.patch(detail_url, update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['specialization'], 'Pediatrics')

    def test_filtering_and_searching(self):
        # Create second profile
        DoctorProfile.objects.create(
            user=self.doctor_user2,
            specialization='Dermatology',
            experience_years=5,
            clinic_name='Skin Care Clinic',
            bio='Skin expert.',
            consultation_fee=100.00
        )

        # Filter by specialization
        response = self.client.get(self.list_url, {'specialization': 'Cardiology'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['specialization'], 'Cardiology')

        # Filter by fee range
        response = self.client.get(self.list_url, {'min_fee': 120.00})
        self.assertEqual(len(response.data), 1)
        self.assertEqual(float(response.data[0]['consultation_fee']), 150.00)

        # Search on name/specialization
        response = self.client.get(self.list_url, {'search': 'Skin'})
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['specialization'], 'Dermatology')

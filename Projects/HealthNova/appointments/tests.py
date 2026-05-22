from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from datetime import date, timedelta
from doctors.models import DoctorProfile
from appointments.models import Appointment

User = get_user_model()

class AppointmentTests(APITestCase):
    def setUp(self):
        # Create users
        self.admin = User.objects.create_user(
            username='admin_user', password='password', email='admin@test.com', role=User.Role.ADMIN
        )
        self.doc_user = User.objects.create_user(
            username='doc_user', password='password', email='doc@test.com', role=User.Role.DOCTOR
        )
        self.patient1 = User.objects.create_user(
            username='patient1', password='password', email='p1@test.com', role=User.Role.PATIENT
        )
        self.patient2 = User.objects.create_user(
            username='patient2', password='password', email='p2@test.com', role=User.Role.PATIENT
        )

        # Create doctor profile
        self.doctor = DoctorProfile.objects.create(
            user=self.doc_user,
            specialization='General Medicine',
            clinic_name='Health Clinic',
            consultation_fee=50.00
        )

        self.list_url = reverse('appointment-list')
        self.appt_date = date.today() + timedelta(days=1)
        self.time_slot = "10:00"

    def test_patient_booking_success(self):
        self.client.force_authenticate(user=self.patient1)
        data = {
            'doctor': self.doctor.id,
            'date': self.appt_date,
            'time_slot': self.time_slot,
            'reason': 'Regular checkup'
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'PENDING')
        self.assertEqual(Appointment.objects.count(), 1)

    def test_past_date_booking_fails(self):
        self.client.force_authenticate(user=self.patient1)
        data = {
            'doctor': self.doctor.id,
            'date': date.today() - timedelta(days=1),
            'time_slot': self.time_slot
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('date', response.data)

    def test_double_booking_prevention(self):
        # Book the first appointment
        Appointment.objects.create(
            doctor=self.doctor, patient=self.patient1, date=self.appt_date, time_slot=self.time_slot
        )

        # Attempt to book the same slot with another patient
        self.client.force_authenticate(user=self.patient2)
        data = {
            'doctor': self.doctor.id,
            'date': self.appt_date,
            'time_slot': self.time_slot
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_rebook_cancelled_slot(self):
        # Book and cancel the first appointment
        appt = Appointment.objects.create(
            doctor=self.doctor, patient=self.patient1, date=self.appt_date, time_slot=self.time_slot,
            status=Appointment.Status.CANCELLED
        )

        # Attempt to book the same slot again (should succeed since first was cancelled)
        self.client.force_authenticate(user=self.patient2)
        data = {
            'doctor': self.doctor.id,
            'date': self.appt_date,
            'time_slot': self.time_slot
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_patient_cancellation_only(self):
        appt = Appointment.objects.create(
            doctor=self.doctor, patient=self.patient1, date=self.appt_date, time_slot=self.time_slot
        )
        detail_url = reverse('appointment-detail', args=[appt.id])

        self.client.force_authenticate(user=self.patient1)
        
        # Try to modify fields other than status (should fail)
        response = self.client.patch(detail_url, {'time_slot': '11:00'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Try to confirm status (should fail)
        response = self.client.patch(detail_url, {'status': 'CONFIRMED'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Try to cancel status (should succeed)
        response = self.client.patch(detail_url, {'status': 'CANCELLED'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        appt.refresh_from_db()
        self.assertEqual(appt.status, 'CANCELLED')

    def test_doctor_update_rbac(self):
        appt = Appointment.objects.create(
            doctor=self.doctor, patient=self.patient1, date=self.appt_date, time_slot=self.time_slot
        )
        detail_url = reverse('appointment-detail', args=[appt.id])

        self.client.force_authenticate(user=self.doc_user)

        # Doctor tries to modify time_slot (should fail)
        response = self.client.patch(detail_url, {'time_slot': '11:00'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Doctor confirms (should succeed)
        response = self.client.patch(detail_url, {'status': 'CONFIRMED'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        appt.refresh_from_db()
        self.assertEqual(appt.status, 'CONFIRMED')

    def test_list_queryset_filters(self):
        # Create user with role doctor
        doc_user2 = User.objects.create_user(
            username='doc_user2', password='password', email='doc2@test.com', role=User.Role.DOCTOR
        )
        doctor2 = DoctorProfile.objects.create(
            user=doc_user2, specialization='Pediatrics', clinic_name='Ped Clinic'
        )

        # Appt 1: doctor 1, patient 1
        appt1 = Appointment.objects.create(
            doctor=self.doctor, patient=self.patient1, date=self.appt_date, time_slot="09:00"
        )
        # Appt 2: doctor 2, patient 2
        appt2 = Appointment.objects.create(
            doctor=doctor2, patient=self.patient2, date=self.appt_date, time_slot="10:00"
        )

        # Patient 1 listing (should only see appt1)
        self.client.force_authenticate(user=self.patient1)
        response = self.client.get(self.list_url)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], appt1.id)

        # Doctor 1 listing (should only see appt1)
        self.client.force_authenticate(user=self.doc_user)
        response = self.client.get(self.list_url)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], appt1.id)

        # Admin listing (should see all)
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(self.list_url)
        self.assertEqual(len(response.data), 2)

import json
from django.test import TestCase, Client
from django.urls import reverse
from .models import Doctor

class DoctorModelTest(TestCase):
    def setUp(self):
        self.doctor = Doctor.objects.create(
            name="Alice Smith",
            specialty="Cardiologist",
            clinic_name="Heart Health Clinic",
            address="123 Main St, San Francisco, CA 94102",
            latitude=37.7749,
            longitude=-122.4194,
            phone_number="415-555-1234",
            email="alice@hearthealth.example.com",
            rating=4.85,
            website="https://hearthealth.example.com"
        )

    def test_doctor_creation(self):
        self.assertTrue(isinstance(self.doctor, Doctor))
        self.assertEqual(str(self.doctor), "Dr. Alice Smith - Cardiologist")

    def test_doctor_fields(self):
        self.assertEqual(self.doctor.name, "Alice Smith")
        self.assertEqual(self.doctor.rating, 4.85)

    def test_default_rating(self):
        doctor_no_rating = Doctor.objects.create(
            name="Bob Jones",
            specialty="Pediatrician",
            clinic_name="SF Pediatrics",
            address="456 Oak St, San Francisco, CA 94103",
            phone_number="415-555-5678"
        )
        self.assertEqual(doctor_no_rating.rating, 5.0)


class DoctorViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        
        # Clear doctors from migration to have clean test state
        Doctor.objects.all().delete()
        
        # Create test doctors
        self.doc1 = Doctor.objects.create(
            name="Alice Smith",
            specialty="Cardiologist",
            clinic_name="Heart Health Clinic",
            address="123 Main St, San Francisco, CA 94102",
            latitude=37.774900,
            longitude=-122.419400,
            phone_number="415-555-1234",
            rating=4.8
        )
        self.doc2 = Doctor.objects.create(
            name="Bob Jones",
            specialty="Pediatrician",
            clinic_name="SF Pediatrics",
            address="456 Oak St, San Francisco, CA 94103",
            latitude=37.770000,
            longitude=-122.420000,
            phone_number="415-555-5678",
            rating=4.5
        )

    def test_index_view(self):
        response = self.client.get(reverse('map_app:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'map_app/index.html')
        self.assertIn('google_maps_api_key', response.context)
        self.assertIn('specialties', response.context)

    def test_api_doctors_list_all(self):
        response = self.client.get(reverse('map_app:api_doctors'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 2)
        
        # Verify structure
        doc_names = [d['name'] for d in data]
        self.assertIn("Alice Smith", doc_names)
        self.assertIn("Bob Jones", doc_names)

    def test_api_doctors_list_filter_specialty(self):
        response = self.client.get(reverse('map_app:api_doctors') + '?specialty=Cardiologist')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['name'], "Alice Smith")

    def test_api_doctors_list_filter_query(self):
        # Search by doctor name
        response = self.client.get(reverse('map_app:api_doctors') + '?q=Jones')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['name'], "Bob Jones")
        
        # Search by clinic name
        response = self.client.get(reverse('map_app:api_doctors') + '?q=Heart')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['name'], "Alice Smith")

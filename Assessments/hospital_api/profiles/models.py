from django.db import models
from django.contrib.auth.models import User

SPECIALTY_CHOICES = [
    ('Allergy and Immunology', 'Allergy and Immunology'),
    ('Anesthesiology', 'Anesthesiology'),
    ('Cardiology', 'Cardiology'),
    ('Cardiothoracic Surgery', 'Cardiothoracic Surgery'),
    ('Dermatology', 'Dermatology'),
    ('Endocrinology', 'Endocrinology'),
    ('Emergency Medicine', 'Emergency Medicine'),
    ('Family Medicine', 'Family Medicine'),
    ('Gastroenterology', 'Gastroenterology'),
    ('General Surgery', 'General Surgery'),
    ('Geriatrics', 'Geriatrics'),
    ('Hematology', 'Hematology'),
    ('Infectious Disease', 'Infectious Disease'),
    ('Internal Medicine', 'Internal Medicine'),
    ('Nephrology', 'Nephrology'),
    ('Neurology', 'Neurology'),
    ('Neurosurgery', 'Neurosurgery'),
    ('Obstetrics and Gynecology', 'Obstetrics and Gynecology'),
    ('Oncology', 'Oncology'),
    ('Ophthalmology', 'Ophthalmology'),
    ('Orthopedic Surgery', 'Orthopedic Surgery'),
    ('Otolaryngology (ENT)', 'Otolaryngology (ENT)'),
    ('Pathology', 'Pathology'),
    ('Pediatrics', 'Pediatrics'),
    ('Physical Medicine and Rehabilitation', 'Physical Medicine and Rehabilitation'),
    ('Plastic Surgery', 'Plastic Surgery'),
    ('Psychiatry', 'Psychiatry'),
    ('Pulmonology', 'Pulmonology'),
    ('Radiology', 'Radiology'),
    ('Rheumatology', 'Rheumatology'),
    ('Urology', 'Urology'),
    ('Vascular Surgery', 'Vascular Surgery'),
    ('Other', 'Other'),
]

class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile', null=True, blank=True)
    name = models.CharField(max_length=255)
    specialty = models.CharField(max_length=255, choices=SPECIALTY_CHOICES, default='Other')
    experience_years = models.PositiveIntegerField(default=0)
    contact_number = models.CharField(max_length=20)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.name} - {self.specialty}"


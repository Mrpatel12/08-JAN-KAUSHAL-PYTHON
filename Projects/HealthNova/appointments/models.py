from django.db import models
from django.conf import settings
from doctors.models import DoctorProfile

class Appointment(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        CONFIRMED = 'CONFIRMED', 'Confirmed'
        CANCELLED = 'CANCELLED', 'Cancelled'
        COMPLETED = 'COMPLETED', 'Completed'

    doctor = models.ForeignKey(
        DoctorProfile,
        on_delete=models.CASCADE,
        related_name='appointments'
    )
    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='appointments',
        limit_choices_to={'role': 'PATIENT'}
    )
    date = models.DateField()
    time_slot = models.CharField(max_length=10)  # e.g., "09:00", "10:00", "14:30"
    status = models.CharField(
        max_length=15,
        choices=Status.choices,
        default=Status.PENDING
    )
    reason = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-date', '-time_slot')
        constraints = [
            models.UniqueConstraint(
                fields=['doctor', 'date', 'time_slot'],
                condition=~models.Q(status='CANCELLED'),
                name='unique_active_doctor_appointment_slot'
            )
        ]

    def __str__(self):
        return f"Appt on {self.date} at {self.time_slot} with Dr. {self.doctor.user.username}"

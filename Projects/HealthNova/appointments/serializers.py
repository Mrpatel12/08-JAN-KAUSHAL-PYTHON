from rest_framework import serializers
from datetime import date
from .models import Appointment
from doctors.serializers import DoctorProfileSerializer
from users.serializers import UserSerializer

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ('id', 'doctor', 'patient', 'date', 'time_slot', 'status', 'reason', 'created_at', 'updated_at')
        read_only_fields = ('patient', 'status', 'created_at', 'updated_at')

    def validate_date(self, value):
        if value < date.today():
            raise serializers.ValidationError("Appointment date cannot be in the past.")
        return value

    def validate(self, attrs):
        doctor = attrs.get('doctor')
        date_val = attrs.get('date')
        time_slot = attrs.get('time_slot')

        queryset = Appointment.objects.filter(
            doctor=doctor,
            date=date_val,
            time_slot=time_slot
        ).exclude(status=Appointment.Status.CANCELLED)

        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise serializers.ValidationError(
                "This time slot is already booked for this doctor."
            )
        return attrs

class AppointmentReadSerializer(serializers.ModelSerializer):
    doctor = DoctorProfileSerializer(read_only=True)
    patient = UserSerializer(read_only=True)

    class Meta:
        model = Appointment
        fields = ('id', 'doctor', 'patient', 'date', 'time_slot', 'status', 'reason', 'created_at', 'updated_at')

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import DoctorProfile
from users.serializers import UserSerializer

User = get_user_model()

class DoctorProfileSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(source='user', read_only=True)
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True
    )

    class Meta:
        model = DoctorProfile
        fields = (
            'id',
            'user',
            'user_details',
            'specialization',
            'experience_years',
            'clinic_name',
            'bio',
            'consultation_fee'
        )

    def validate_user(self, value):
        if DoctorProfile.objects.filter(user=value).exists():
            raise serializers.ValidationError("This user already has a doctor profile.")
        return value

    def create(self, validated_data):
        user = validated_data['user']
        if user.role != User.Role.DOCTOR:
            user.role = User.Role.DOCTOR
            user.save(update_fields=['role'])
        return super().create(validated_data)

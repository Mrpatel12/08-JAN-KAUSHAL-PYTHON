import django_filters
from .models import DoctorProfile

class DoctorFilter(django_filters.FilterSet):
    min_experience = django_filters.NumberFilter(field_name="experience_years", lookup_expr='gte')
    max_experience = django_filters.NumberFilter(field_name="experience_years", lookup_expr='lte')
    min_fee = django_filters.NumberFilter(field_name="consultation_fee", lookup_expr='gte')
    max_fee = django_filters.NumberFilter(field_name="consultation_fee", lookup_expr='lte')
    specialization = django_filters.CharFilter(lookup_expr='icontains')
    clinic_name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = DoctorProfile
        fields = ['specialization', 'clinic_name', 'min_experience', 'max_experience', 'min_fee', 'max_fee']

from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import DoctorProfile
from .serializers import DoctorProfileSerializer
from .filters import DoctorFilter
from users.permissions import IsAdminUserRole, IsDoctorOwnerOrAdmin

class DoctorProfileViewSet(viewsets.ModelViewSet):
    queryset = DoctorProfile.objects.select_related('user').all()
    serializer_class = DoctorProfileSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filterset_class = DoctorFilter
    search_fields = ('specialization', 'clinic_name', 'user__first_name', 'user__last_name', 'user__username')
    ordering_fields = ('experience_years', 'consultation_fee')
    ordering = ('-experience_years',)

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [permissions.AllowAny()]
        elif self.action == 'create':
            return [permissions.IsAuthenticated(), IsAdminUserRole()]
        elif self.action in ('update', 'partial_update'):
            return [permissions.IsAuthenticated(), IsDoctorOwnerOrAdmin()]
        elif self.action == 'destroy':
            return [permissions.IsAuthenticated(), IsAdminUserRole()]
        return super().get_permissions()

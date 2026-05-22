from rest_framework import viewsets, permissions, status
from rest_framework.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from .models import Appointment
from .serializers import AppointmentSerializer, AppointmentReadSerializer
from users.permissions import (
    IsPatientUserRole,
    IsAppointmentParticipantOrAdmin
)

class AppointmentViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated, IsAppointmentParticipantOrAdmin)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('date', 'status', 'doctor', 'patient')

    def get_queryset(self):
        user = self.request.user
        if user.role == 'ADMIN':
            return Appointment.objects.select_related('doctor__user', 'patient').all()
        elif user.role == 'DOCTOR':
            return Appointment.objects.select_related('doctor__user', 'patient').filter(doctor__user=user)
        else:
            return Appointment.objects.select_related('doctor__user', 'patient').filter(patient=user)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return AppointmentReadSerializer
        return AppointmentSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.IsAuthenticated(), IsPatientUserRole()]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(patient=self.request.user)

    def perform_update(self, serializer):
        user = self.request.user
        new_status = self.request.data.get('status')

        if user.role == 'PATIENT':
            if new_status and new_status != Appointment.Status.CANCELLED:
                raise ValidationError("Patients can only update the status to CANCELLED.")
            # If they try to modify other fields
            writable_keys = {k for k in self.request.data.keys()}
            if writable_keys - {'status'}:
                raise ValidationError("Patients cannot modify appointment details after booking, they can only cancel.")
            serializer.save(status=Appointment.Status.CANCELLED)

        elif user.role == 'DOCTOR':
            if new_status and new_status not in (Appointment.Status.CONFIRMED, Appointment.Status.CANCELLED, Appointment.Status.COMPLETED):
                raise ValidationError("Doctors can only set status to CONFIRMED, CANCELLED, or COMPLETED.")
            writable_keys = {k for k in self.request.data.keys()}
            if writable_keys - {'status'}:
                raise ValidationError("Doctors cannot modify appointment details, they can only update the status.")
            serializer.save(status=new_status)

        else:
            serializer.save()

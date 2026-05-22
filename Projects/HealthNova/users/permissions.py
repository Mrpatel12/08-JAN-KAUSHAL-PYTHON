from rest_framework import permissions

class IsAdminUserRole(permissions.BasePermission):
    """
    Allows access only to Admin users.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'ADMIN'

class IsDoctorUserRole(permissions.BasePermission):
    """
    Allows access only to Doctor users.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'DOCTOR'

class IsPatientUserRole(permissions.BasePermission):
    """
    Allows access only to Patient users.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'PATIENT'

class IsDoctorOwnerOrAdmin(permissions.BasePermission):
    """
    Allows doctors to edit only their own profile, and admins full access.
    """
    def has_object_permission(self, request, view, obj):
        # Admin has full access
        if request.user.role == 'ADMIN':
            return True
        # Doctor can write to their own profile
        return request.user.role == 'DOCTOR' and obj.user == request.user

class IsAppointmentParticipantOrAdmin(permissions.BasePermission):
    """
    Allows access to appointments only for the assigned patient, the doctor, or admins.
    """
    def has_object_permission(self, request, view, obj):
        return (
            request.user.role == 'ADMIN' or
            obj.patient == request.user or
            obj.doctor.user == request.user
        )

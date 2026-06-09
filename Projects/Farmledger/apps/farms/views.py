from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Farm
from .serializers import FarmSerializer


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class FarmViewSet(viewsets.ModelViewSet):
    queryset = Farm.objects.all().select_related('owner')
    serializer_class = FarmSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated(),]

    def get_queryset(self):
        # users see only their farms by default
        return Farm.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
        farm = self.get_object()
        # placeholder stats
        data = {
            'farm_id': str(farm.id),
            'total_crops': farm.crops.count(),
            'total_expenses': 0,
            'total_revenue': 0,
        }
        return Response(data)

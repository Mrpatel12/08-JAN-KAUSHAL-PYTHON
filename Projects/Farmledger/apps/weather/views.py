from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import WeatherObservation
from .serializers import WeatherObservationSerializer


class WeatherObservationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = WeatherObservation.objects.all()
    serializer_class = WeatherObservationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return WeatherObservation.objects.filter(farm__owner=user)

    @action(detail=False, methods=['post'])
    def refresh(self, request):
        farm_id = request.data.get('farm_id')
        location = request.data.get('location', '')
        if not farm_id:
            return Response({'error': 'farm_id required'}, status=400)
        # Import task lazily so Django management commands don't require Celery
        try:
            from .tasks import fetch_weather_for_farm
            fetch_weather_for_farm.delay(farm_id, location)
        except Exception:
            return Response({'dispatched': False, 'error': 'celery_not_available'}, status=503)
        return Response({'dispatched': True})

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WeatherObservationViewSet

router = DefaultRouter()
router.register('observations', WeatherObservationViewSet, basename='weather-observation')

urlpatterns = [
    path('', include(router.urls)),
]

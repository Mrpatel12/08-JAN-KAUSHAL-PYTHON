from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import HarvestViewSet

router = DefaultRouter()
router.register(r'harvests', HarvestViewSet, basename='harvest')

urlpatterns = [
    path('', include(router.urls)),
]

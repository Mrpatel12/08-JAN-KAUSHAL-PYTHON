from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DoctorProfileViewSet

router = DefaultRouter()
router.register(r'doctors', DoctorProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

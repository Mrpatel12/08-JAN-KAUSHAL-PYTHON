from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .models import Crop
from .serializers import CropSerializer


class CropViewSet(viewsets.ModelViewSet):
    queryset = Crop.objects.all().select_related('farm')
    serializer_class = CropSerializer

    def get_queryset(self):
        # restrict to crops in farms owned by the user
        return Crop.objects.filter(farm__owner=self.request.user)

    def perform_create(self, serializer):
        # expect `farm_id` in the request data to attach
        farm = None
        farm_id = self.request.data.get('farm_id')
        if farm_id:
            from apps.farms.models import Farm
            farm = Farm.objects.get(id=farm_id, owner=self.request.user)
        serializer.save(farm=farm)

from rest_framework import serializers
from .models import Crop


class CropSerializer(serializers.ModelSerializer):
    farm = serializers.ReadOnlyField(source='farm.id')

    class Meta:
        model = Crop
        fields = ('id', 'farm', 'name', 'variety', 'planted_at', 'expected_harvest_at', 'status', 'area_planted', 'created_at', 'updated_at')
        read_only_fields = ('id', 'farm', 'created_at', 'updated_at')

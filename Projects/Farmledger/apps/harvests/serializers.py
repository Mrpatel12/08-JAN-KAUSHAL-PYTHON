from rest_framework import serializers
from .models import Harvest


class HarvestSerializer(serializers.ModelSerializer):
    farm = serializers.ReadOnlyField(source='farm.id')

    class Meta:
        model = Harvest
        fields = ('id', 'farm', 'crop', 'harvested_at', 'quantity', 'unit', 'revenue', 'notes', 'created_at', 'updated_at')
        read_only_fields = ('id', 'farm', 'created_at', 'updated_at')

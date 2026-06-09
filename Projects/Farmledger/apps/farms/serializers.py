from rest_framework import serializers
from .models import Farm


class FarmSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')

    class Meta:
        model = Farm
        fields = ('id', 'owner', 'name', 'slug', 'location', 'acreage', 'timezone', 'currency', 'status', 'created_at', 'updated_at')
        read_only_fields = ('id', 'owner', 'created_at', 'updated_at')

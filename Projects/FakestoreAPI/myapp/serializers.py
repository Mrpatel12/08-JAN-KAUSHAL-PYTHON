from rest_framework import serializers

class RatingSerializer(serializers.Serializer):
    rate = serializers.FloatField()
    count = serializers.IntegerField()

class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)
    price = serializers.FloatField()
    description = serializers.CharField()
    category = serializers.CharField(max_length=100)
    image = serializers.URLField()
    rating = RatingSerializer()

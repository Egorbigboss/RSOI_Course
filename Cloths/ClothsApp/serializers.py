from rest_framework import serializers
from ClothsApp.models import Cloth


class ClothSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cloth
        fields = [
            'uuid',
            'type_of_cloth',
            'days_for_clearing',
        ]

    def create(self, validated_data):
        new = Cloth.objects.create(**validated_data)
        return new

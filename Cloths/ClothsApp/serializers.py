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

    def update(self, instance: Cloth, validated_data):
        instance.type_of_cloth = validated_data.get('type_of_cloth', instance.type_of_cloth)
        instance.days_for_clearing = validated_data.get('days_for_clearing', instance.days_for_clearing)
        instance.save()
        return instance

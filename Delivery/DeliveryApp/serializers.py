from rest_framework import serializers
from DeliveryApp.models import DeliveryList


class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryList
        fields = [
            'uuid',
            'order_uuid',
            'user_id',
            'status',
        ]

    def create(self, validated_data):
        new = DeliveryList.objects.create(**validated_data)
        return new

    def update(self, instance: DeliveryList, validated_data):
        instance.order_uuid = validated_data.get('order_uuid', instance.order_uuid)
        instance.user_id = validated_data.get('user_id', instance.user_id)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance

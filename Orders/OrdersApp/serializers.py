from rest_framework import serializers
from OrdersApp.models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
             'belongs_to_user_id',
             'uuid',
             'text',
             'cloth_uuid',
        ]

    def create(self, validated_data):
        new = Order.objects.create(**validated_data)
        return new

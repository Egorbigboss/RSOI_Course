from rest_framework import serializers
from OrdersApp.models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'uuid',
            'belongs_to_user_id',
            'text',
            'type_of_cloth',
            'cloth_uuid',
            'date_of_creation'
        ]

    def create(self, validated_data):
        new = Order.objects.create(**validated_data)
        return new

from rest_framework import serializers
from StatisticsApp.models import Stats


class StatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stats
        fields = [
            'uuid',
            'type_of_object',
            'text',
            'count'
        ]

    def create(self, validated_data):
        new = Stats.objects.create(**validated_data)
        return new

    def update(self, instance: Stats, validated_data):
        instance.count = validated_data.get('count', instance.count)
        instance.type_of_object = validated_data.get('type_of_object', instance.type_of_object)
        instance.text = validated_data.get('text', instance.text)
        # instance.days_for_clearing = validated_data.get('days_for_clearing', instance.days_for_clearing)
        instance.save()
        return instance

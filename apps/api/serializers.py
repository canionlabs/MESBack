from rest_framework import serializers

from apps.processor.models import IceProduction


class IceProductionSerializer(serializers.ModelSerializer):
    class Meta:
        model = IceProduction
        fields = ('ice_type', 'weight', 'date', 'hour')

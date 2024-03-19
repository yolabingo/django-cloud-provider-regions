from rest_framework import serializers
from .models import CloudProvider, CloudRegion, CloudAvailabilityZone


class CloudProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = CloudProvider
        fields = "__all__"


class CloudRegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CloudRegion
        fields = "__all__"


class CloudAvailabilityZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = CloudAvailabilityZone
        fields = "__all__"

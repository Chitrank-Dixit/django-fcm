from rest_framework import serializers
from fcm.utils import get_device_model
Device = get_device_model()


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'

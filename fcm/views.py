from rest_framework import viewsets
from fcm.utils import get_device_model
from fcm.serializers import DeviceSerializer
Device = get_device_model()


class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

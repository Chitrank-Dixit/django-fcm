from rest_framework import viewsets, status, response
from fcm.utils import get_device_model
from fcm.serializers import DeviceSerializer
Device = get_device_model()


class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

    def perform_create(self, serializer):
        try:
            device = Device.objects.get(dev_id=serializer.validated_data["dev_id"])
        except Device.DoesNotExist:
            device = Device(dev_id=serializer.validated_data["dev_id"])
        device.is_active = True
        device.reg_id = serializer.validated_data["reg_id"]
        device.save()

    def destroy(self, request, *args, **kwargs):
        try:
            instance = Device.objects.get(dev_id=kwargs["pk"])
            self.perform_destroy(instance)
            return response.Response(status=status.HTTP_200_OK)
        except Device.DoesNotExist:
            return response.Response(status=status.HTTP_404_NOT_FOUND)

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

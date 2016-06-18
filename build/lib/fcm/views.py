from django.shortcuts import render
from rest_framework import viewsets
from device.models import Device
from device.serializers import DeviceSerializer


class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

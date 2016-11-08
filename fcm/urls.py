from django.conf.urls import url, include

from rest_framework import routers
from fcm.views import DeviceViewSet

router = routers.DefaultRouter()
router.register(r'devices', DeviceViewSet)

urlpatterns = [
    url(r'v1/', include(router.urls))

]

Api key authentication
======================

Allows you to manage access to the FCM api using one of the available ``tastypie`` authentication methods - `ApiKeyAuthentication`.

.. _django-tastypie Authentication: http://django-tastypie.readthedocs.org/en/latest/authentication.html

.. note:: I strongly recommend see `django-tastypie Authentication`_ docs.


Adding authentication requires `djangorestframework` added to your `INSTALLED_APPS` in the ``settings.py`` file:

.. code-block:: python

    INSTALLED_APPS = [
          ...
          'fcm',
          'rest_framework',
      ]


Adding user field
--------------

You need to extend `Device` model and add user field. (See :ref:`extending_device`)

.. code-block:: python

    # your_app/models.py
    from django.conf import settings
    from django.db import models
    from fcm.models import AbstractDevice

    class MyDevice(AbstractDevice):

        user = models.ForeignKey(settings.AUTH_USER_MODEL)


Add appropriate path to the ``settings.py`` file:

.. code-block:: python

    FCM_DEVICE_MODEL = 'your_app.models.MyDevice'


Serializer class
-----------------

In your application , you can create the serializer, or customize it according the extra field you have included in your `Device` model.

.. code-block:: python

    from rest_framework import serializers
    from fcm.models import Device
    
    
    class DeviceSerializer(serializers.ModelSerializer):
        class Meta:
            model = Device
            fields = ('dev_id','reg_id','name','is_active')


View class
--------------

In your application, you need to create your view either through `ModelViewSet` or can user or override methods as specified in django-rest-framework documentation.


.. code-block:: python

    from rest_framework import viewsets
    from fcm.models import Device
    from fcm.serializers import DeviceSerializer
    
    
    class DeviceViewSet(viewsets.ModelViewSet):
        queryset = Device.objects.all()
        serializer_class = DeviceSerializer



You need to hook your viewset class up in your ``urls.py`` file:

.. code-block:: python

    # your_app/urls.py
    from django.conf.urls import url, include

    from rest_framework import routers
    from fcm.views import DeviceViewSet

    router = routers.DefaultRouter()
    router.register(r'devices', DeviceViewSet)

    urlpatterns = [
        url(r'^v1/', include(router.urls))

    ]



Include your ``urls.py`` file in the main URL router:

.. code-block:: python

    # urls.py
    from django.conf.urls import include, url

    urlpatterns = [
        url(r'', include('your_app.urls')),
    ]





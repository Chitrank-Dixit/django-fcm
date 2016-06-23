Quickstart
==========

#. Install package via `pip`:

   .. code-block:: bash

      $ pip install django-fcm

#. Add `django-fcm` resources to your URL router::

      # urls.py
      from django.conf.urls import include, url

      urlpatterns = [
          url(r'', include('fcm.urls')),
      ]


   To check fcm urls just use the following command:

   .. code-block:: bash

        $ python manage.py fcm_urls

        FCM urls:
        * Register device
            /fcm/v1/devices/
        * Unregister device
            /fcm/v1/devices/{id}/


#. Configure `django-dcm` in your ``settings.py`` file::

      INSTALLED_APPS = [
          # ...
          'fcm',
      ]

      FCM_APIKEY = "<api_key>"

.. note:: To obtain api key go to https://code.google.com/apis/console and grab the key for the server app.

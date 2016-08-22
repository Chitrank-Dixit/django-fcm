django-fcm
==========

Firebase Cloud Messaging Server in Django

Quickstart
----------

Install the package via ``pip``::

    pip install django-gcm  --process-dependency-links

Add ``fcm`` to ``INSTALLED_APPS`` in ``settings.py``

Add ``FCM_APIKEY`` to ``settings.py`` file:

.. code-block:: python

    FCM_APIKEY = "<api_key>"


Add ``fcm urls`` to ``urls.py`` file:

.. code-block:: python

    urlpatterns = [
      ...
      url(r'', include('fcm.urls')),
      ...
    ]


Documentation: `https://django-fcm.readthedocs.org <https://django-fcm.readthedocs.org>`_

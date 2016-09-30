django-fcm
==========
.. image:: https://badge.fury.io/py/django-fcm.svg
    :target: https://badge.fury.io/py/django-fcm

Firebase Cloud Messaging Server in Django

Quickstart
----------

Install the package via ``pip``::

    pip install django-fcm  --process-dependency-links
    


Add ``fcm`` to ``INSTALLED_APPS`` in ``settings.py``

.. code-block:: python

   INSTALLED_APPS = [
       ....,
       fcm
   ]

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


Python 3 support
----------------
``django-fcm`` is fully compatible with Python 3.4 & 3.5

Django Support
----------------
``django-fcm`` is fully compatible with Django 1.8, 1.9 and 1.10

Django Rest Framework
----------------
``django-fcm`` is fully compatible with django-rest-framework 3.3.2.


Documentation: `https://django-fcm.readthedocs.org <https://django-fcm.readthedocs.org>`_

Sending messages
================

Using ``console``:

.. code-block:: bash

    # Get the list of devices
    $ python manage.py fcm_messenger --devices
    > Devices list:
    > (#1) My phone

    # python manage.py fcm_messenger <device_id> <message> [--collapse-key <key>]
    $ python manage.py fcm_messenger 1 'my test message'

Using ``Django orm``::

    from fcm.models import get_device_model
    Device = get_device_model()

    my_phone = Device.objects.get(name='My phone')
    my_phone.send_message({'message':'my test message'}, collapse_key='something')

``collapse_key`` parameter is optional (default message).

If you want to send additional arguments like ``delay_while_idle`` or other, add them as named variables e.g.::

    my_phone.send_message({'message':'my test message'}, delay_while_idle=True, time_to_live=5)

.. _Lifetime of a Message: https://developer.android.com/google/gcm/server.html#lifetime
.. _Sending a downstream message: https://developer.android.com/google/gcm/server-ref.html#send-downstream

.. note:: For more information, see `Lifetime of a Message`_ and `Sending a downstream message`_ docs.


Multicast message
-----------------

``django-fcm`` supports sending messages to multiple devices at once. E.g.::

    from fcm.models import get_device_model
    Device = get_device_model()
    
    Device.objects.all().send_message({'message':'my test message'})


Topic messaging
-----------------------

``django-fcm`` supports sending messages to multiple devices that have opted in to a particular fcm topic::

    from fcm.api import FCMMessage

    FCMMessage().send({'message':'my test message'}, to='/topics/my-topic')

.. _Send messages to topics: https://developers.google.com/cloud-messaging/topic-messaging

.. note:: For more information, see `Send messages to topics`_.

import json
import requests
from django.core.exceptions import ImproperlyConfigured
from django.utils.encoding import force_text
from django.conf import settings
from django.utils.module_loading import import_module


def load_object(object_path):

    module_path, object_name = object_path.rsplit('.', 1)
    module = import_module(module_path)

    return getattr(module, object_name)


def get_device_model():
    return load_object(settings.FCM_DEVICE_MODEL)


class FCMMessage(object):

    def __init__(self):
        self.api_key = settings.FCM_APIKEY

        if not self.api_key:
            raise ImproperlyConfigured(
                "You haven't set the 'FCM_APIKEY' setting yet.")

    def _chunks(self, items, limit):
        """
            Yield successive chunks from list \a items with a minimum size \a limit
        """
        for i in range(0, len(items), limit):
            yield items[i:i + limit]

    def send(self, data, registration_ids=None, **kwargs):
        """
        Send a FCM message for one or more devices, using json data
        registration_ids: A list with the devices which will be receiving a message
        data: The dict data which will be send
        Optional params e.g.:
            collapse_key: A string to group messages
        For more info see the following documentation:
        https://developer.android.com/google/fcm/server-ref.html#send-downstream
        """

        if not isinstance(data, dict):
            data = {'msg': data}

        registration_ids = registration_ids or []

        if len(registration_ids) > settings.FCM_MAX_RECIPIENTS:
            ret = []
            for chunk in self._chunks(
                    registration_ids, settings.FCM_MAX_RECIPIENTS):
                ret.append(self.send(data, registration_ids=chunk, **kwargs))
            return ret

        values = {
            'data': data,
            'collapse_key': 'message'}
        if registration_ids:
            values.update({'registration_ids': registration_ids})
        values.update(kwargs)

        values = json.dumps(values)

        headers = {
            'UserAgent': "FCM-Server",
            'Content-Type': 'application/json',
            'Authorization': 'key=' + self.api_key}

        response = requests.post(
            url="https://fcm.googleapis.com/fcm/send",
            data=values, headers=headers)

        response.raise_for_status()
        return registration_ids, json.loads(force_text(response.content))

class FCMMessage(FCMMessage):
    FCM_INVALID_ID_ERRORS = ['InvalidRegistration',
                             'NotRegistered',
                             'MismatchSenderId']

    def send(self, data, registration_ids=None, **kwargs):
        response = super(FCMMessage, self).send(
            data, registration_ids=registration_ids, **kwargs)
        chunks = [response] if not isinstance(response, list) else response
        for chunk in chunks:
            self.post_send(*chunk)
        return response

    def post_send(self, registration_ids, response):
        if response.get('failure'):
            invalid_messages = dict(filter(
                lambda x: x[1].get('error') in self.FCM_INVALID_ID_ERRORS,
                zip(registration_ids, response.get('results'))))

            regs = list(invalid_messages.keys())
            for device in get_device_model().objects.filter(reg_id__in=regs):
                device.mark_inactive(
                    error_message=invalid_messages[device.reg_id]['error'])
import json
from django.core.exceptions import ImproperlyConfigured
from django.utils.encoding import force_text
from django.conf import settings
import requests

__author__ = 'chitrankdixit'

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
        https://developer.android.com/google/gcm/server-ref.html#send-downstream
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

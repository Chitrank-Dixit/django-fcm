import json
import requests
from django.apps import apps
from django.core.exceptions import ImproperlyConfigured
from django.utils.encoding import force_text
from django.conf import settings
from django.utils.module_loading import import_module

DEFAULT_FCM_DEVICE_MODEL = 'fcm.Device'


def get_device_model():
    model = getattr(settings, "FCM_DEVICE_MODEL", DEFAULT_FCM_DEVICE_MODEL)
    try:
        return apps.get_model(model)
    except ValueError:
        raise ImproperlyConfigured("FCM_DEVICE_MODEL must be of the form 'app_label.model_name'")
    except LookupError:
        raise ImproperlyConfigured(
            "FCM_DEVICE_MODEL refers to model '%s' that has not been installed" % settings.FCM_DEVICE_MODEL
        )


class NotificationMessage(object):

    '''
    Background Notification Message object.
    '''

    FCM_NOTIFICATION_KEYS = getattr(settings, "FCM_NOTIFICATION_KEYS", None)

    '''
    Set default values to FCM notification keys inside settings.
    '''

    # FCM_NOTIFICATION_KEYS = {
    #     "title": "My title for all notifications",
    #     "icon": "My icon for all android notifications",
    #     "sound": "My sound for all notifications",
    #     "color": "My color for all android notifications icon #ffffff",
    #     "tag": "My tag for all notifications",
    #     "click_action": "My action when notification is pressed",
    #     "body_loc_key": "",
    #     "body_loc_args": "",
    #     "title_loc_key": "",
    #     "title_loc_args": "",
    #     "badge: "Badge for all my iOS notifications"
    # }

    def __init__(self, message):
        self.message = message

    def create_notification_message(self):
        '''
        Background Notification Message constructor with default values from settings (not mandatory)
        '''
        notification_message = self.message.copy()
        if self.FCM_NOTIFICATION_KEYS is not None:
            notification_keys = \
                {key: val for key, val in self.FCM_NOTIFICATION_KEYS.items() if key not in notification_message}
            notification_message.update(notification_keys)
        return notification_message


class BaseFCMMessage(object):

    def __init__(self):
        """
        you will not reach to test self.api_key if it is not set in settings...
        """
        try:
            self.api_key = settings.FCM_APIKEY
        except AttributeError:
            raise ImproperlyConfigured(
                "You haven't set the 'FCM_APIKEY' setting yet.")

        """
        accessing settings.FCM_MAX_RECIPIENTS if not set
        will crash the app, it can be set to 1 by default
        """
        try:
            self.max_recipients = settings.FCM_MAX_RECIPIENTS
        except AttributeError:
            # some kind of warning would be nice
            print("Using default settings.FCM_MAX_RECIPIENTS value 1. Change it via settings")
            self.max_recipients = 1

    def _chunks(self, items, limit):
        """
            Yield successive chunks from list \a items with a minimum size \a limit
        """
        for i in range(0, len(items), limit):
            yield items[i:i + limit]

    def send(self, data, notification=None, registration_ids=None, **kwargs):
        if not isinstance(data, dict):
            data = {'msg': data}

        registration_ids = registration_ids or []

        if len(registration_ids) > self.max_recipients:
            ret = []
            for chunk in self._chunks(
                    registration_ids, settings.FCM_MAX_RECIPIENTS):
                ret.append(self.send(data, notification, registration_ids=chunk, **kwargs))
            return ret

        values = {'data': data}

        if notification is not None:
            notification_obj = NotificationMessage(notification)
            notification_message = notification_obj.create_notification_message()
            values.update({'notification': notification_message})

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


class FCMMessage(BaseFCMMessage):
    FCM_INVALID_ID_ERRORS = ['InvalidRegistration',
                             'NotRegistered',
                             'MismatchSenderId']

    def send(self, data, notification=None, registration_ids=None, **kwargs):
        response = super(FCMMessage, self).send(
            data, notification, registration_ids=registration_ids, **kwargs)
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

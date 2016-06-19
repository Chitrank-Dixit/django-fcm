import logging
from django.conf import settings
from django.db import models
from fcm.utils import load_object, FCMMessage

logger = logging.getLogger(__name__)


class AbstractDevice(models.Model):
    dev_id = models.CharField(verbose_name= ("Device ID"), max_length=50, unique=True,)
    reg_id = models.CharField(verbose_name= ("Registration ID"), max_length=255, unique=True)
    name = models.CharField(verbose_name= ("Name"), max_length=255, blank=True, null=True)
    is_active = models.BooleanField(verbose_name= ("Is active?"), default=False)


    def __str__(self):
        return self.dev_id

    class Meta:
        abstract = True
        verbose_name = ("Device")
        verbose_name_plural = ("Devices")

    def send_message(self, data, **kwargs):
        return FCMMessage().send(
            registration_ids=[self.reg_id], data=data, **kwargs)

    def mark_inactive(self, **kwargs):
        self.is_active = False
        self.save()
        if kwargs.get('error_message'):
            logger.debug("Device %s (%s) marked inactive due to error: %s",
                         self.dev_id, self.name, kwargs['error_message'])


class Device(AbstractDevice):
    pass
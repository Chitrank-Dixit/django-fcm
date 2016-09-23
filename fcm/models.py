import logging
from django.db.models.query import QuerySet
from django.db import models
from fcm.utils import FCMMessage

logger = logging.getLogger(__name__)


class DeviceQuerySet(QuerySet):

    def send_message(self, data, **kwargs):
        if self:
            registration_ids = list(self.values_list("reg_id", flat=True))
            return FCMMessage().send(
                data, registration_ids=registration_ids, **kwargs)


class DeviceManager(models.Manager):

    def get_queryset(self):
        return DeviceQuerySet(self.model)


class AbstractDevice(models.Model):
    dev_id = models.CharField(verbose_name=("Device ID"), max_length=50, unique=True,)
    reg_id = models.CharField(verbose_name=("Registration ID"), max_length=255, unique=True)
    name = models.CharField(verbose_name=("Name"), max_length=255, blank=True, null=True)
    is_active = models.BooleanField(verbose_name=("Is active?"), default=False)

    objects = DeviceManager()

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
    class Meta:
        swappable = 'FCM_DEVICE_MODEL'

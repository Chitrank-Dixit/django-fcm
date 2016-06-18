from django.db import models

# class GCMMessage(api.GCMMessage):
#     GCM_INVALID_ID_ERRORS = ['InvalidRegistration',
#                              'NotRegistered',
#                              'MismatchSenderId']
#
#     def send(self, data, registration_ids=None, **kwargs):
#         response = super(GCMMessage, self).send(
#             data, registration_ids=registration_ids, **kwargs)
#         chunks = [response] if not isinstance(response, list) else response
#         for chunk in chunks:
#             self.post_send(*chunk)
#         return response
#
#     def post_send(self, registration_ids, response):
#         if response.get('failure'):
#             invalid_messages = dict(filter(
#                 lambda x: x[1].get('error') in self.GCM_INVALID_ID_ERRORS,
#                 zip(registration_ids, response.get('results'))))
#
#             regs = list(invalid_messages.keys())
#             for device in get_device_model().objects.filter(reg_id__in=regs):
#                 device.mark_inactive(
#                     error_message=invalid_messages[device.reg_id]['error'])

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

    # def send_message(self, data, **kwargs):
    #     return GCMMessage().send(
    #         registration_ids=[self.reg_id], data=data, **kwargs)
    #
    # def mark_inactive(self, **kwargs):
    #     self.is_active = False
    #     self.save()
    #     if kwargs.get('error_message'):
    #         logger.debug("Device %s (%s) marked inactive due to error: %s",
    #                      self.dev_id, self.name, kwargs['error_message'])


class Device(AbstractDevice):
    pass
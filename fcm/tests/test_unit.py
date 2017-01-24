from django.test import TestCase
from fcm.models import Device


class DeviceTest(TestCase):
    def setUp(self):
        self.dev_id = "12345"
        self.reg_id = "12345"
        self.name = "fcm_test_device"
        self.is_active = True


    def create_device(self):
        self.device = Device.objects.create(
            dev_id = self.dev_id,
            reg_id = self.reg_id,
            name = self.name,
            is_active = self.is_active
        )

        #self.assertEqual(self.device.id, self.tracking_source_name)

    def send_message(self):
        self.device.send_message()



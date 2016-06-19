from django.core.management.base import NoArgsCommand
from django.core.urlresolvers import reverse
from fcm.views import DeviceViewSet


class Command(NoArgsCommand):
    help = "Show FCM urls"

    def show_line(self):
        self.stdout.write("%s\n" % ("-" * 30))

    def handle_noargs(self, **options):
        url_kwargs = {'api_name': 'v1'}
        # TODO add proper url resolvers
        #register_url = reverse('devices', kwargs=url_kwargs)
        #unregister_url = reverse('devices', kwargs=url_kwargs)
        register_url = 'fcm/v1/devices'
        unregister_url = 'fcm/v1/devices/<pk>'
        self.show_line()
        self.stdout.write("FCM urls:\n")
        self.stdout.write("* Register device\n    %s\n" % register_url)
        self.stdout.write("* Unregister device\n    %s\n" % unregister_url)
        self.show_line()
import datetime

from django.core.management import BaseCommand

from main.models import ServiceProvider, ServiceProviderSchedule, DAY_CHOICES


class Command(BaseCommand):

    def handle(self, *args, **options):
        for service_provider in ServiceProvider.objects.all():
            for day in dict(DAY_CHOICES).keys():
                ServiceProviderSchedule.objects.create(
                    service_provider=service_provider,
                    day=day,
                    time_start=datetime.time(hour=9),
                    time_end=datetime.time(hour=18)
                )
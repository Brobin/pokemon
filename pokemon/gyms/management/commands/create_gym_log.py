import cfscrape

from collections import Counter

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone

from pokemon.gyms.models import GymLog


class Command(BaseCommand):

    def handle(self, *args, **options):
        data = requests.get(settings.API_URL).json()
        GymLog.objects.create(
            created_at=timezone.now(),
            mystic=data['mystic'],
            valor=data['valor'],
            instinct=data['isntinct'],
        )

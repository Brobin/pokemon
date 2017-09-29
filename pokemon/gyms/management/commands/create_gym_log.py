import cfscrape

from collections import Counter

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone

from pokemon.gyms.models import GymLog


class Command(BaseCommand):

    def handle(self, *args, **options):
        scraper = cfscrape.create_scraper()
        data = scraper.get(settings.API_URL)
        print(data)
        gyms = data.json()['gyms']
        teams = [gyms[key]['team_id'] for key in gyms]
        counter = dict(Counter(teams))
        GymLog.objects.create(
            created_at=timezone.now(),
            mystic=counter[1],
            valor=counter[2],
            instinct=counter[3],
        )

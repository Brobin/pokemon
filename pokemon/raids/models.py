from django.db import models
from django.urls import reverse
from copy import copy

from ..trainers.models import Trainer
from ..trainers.constants import POKEMON, POKEMON_CHOICES

TIER_1 = 1
TIER_2 = 2
TIER_3 = 3
TIER_4 = 4
TIER_5 = 5
RAID_TIERS = (
    (TIER_1, 'Tier 1'),
    (TIER_2, 'Tier 2'),
    (TIER_3, 'Tier 3'),
    (TIER_4, 'Tier 4'),
    (TIER_5, 'Tier 5')
)


class Raid(models.Model):
    tier = models.IntegerField(choices=RAID_TIERS)
    pokemon = models.IntegerField(choices=POKEMON_CHOICES)
    active = models.BooleanField(default=False)

    @property
    def url(self):
        return reverse('raid-detail', kwargs={'number': self.pokemon})

    def leaders(self):
        return self.records.filter(verified=True).order_by('-time_remaining')

    def leader(self):
        return self.leaders().first()

    @property
    def image(self):
        number = str(self.pokemon)
        while len(number) < 3:
            number = '0' + number
        url = number + '-00'
        return 'https://pokemon.gameinfo.io/images/pokemon-go/{0}.png'.format(url)

    def __str__(self, *args, **kwargs):
        return POKEMON[self.pokemon]


class RaidRecord(models.Model):
    raid = models.ForeignKey(Raid, related_name='records', on_delete=models.CASCADE)
    trainer = models.ForeignKey(Trainer, related_name='raid_records', on_delete=models.CASCADE)

    time_remaining = models.IntegerField()
    lineup_screenshot = models.ImageField(upload_to='raids', blank=True, null=True)
    finish_screenshot = models.ImageField(upload_to='raids', blank=True, null=True)
    date = models.DateField()

    verified = models.BooleanField(default=True)

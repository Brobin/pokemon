from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Avg, Sum, Count
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from .trainers.models import Trainer
from .trainers.models import MYSTIC, VALOR, INSTINCT


class StatsView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['stats'] = Trainer.objects.aggregate(
            avg_xp=Avg('xp'),
            sum_xp=Sum('xp'),
            avg_pokemon_caught=Avg('pokemon_caught'),
            sum_pokemon_caught=Sum('pokemon_caught'),
            avg_pokestops_spun=Avg('pokestops_spun'),
            sum_pokestops_spun=Sum('pokestops_spun'),
            avg_pokedex_number=Avg('pokedex_number'),
            sum_kilometers_walked=Sum('kilometers_walked'),
            avg_kilometers_walked=Avg('kilometers_walked'),
            sum_battles_won=Sum('battles_won'),
            avg_battles_won=Avg('battles_won'),
        )
        context['xp_leaders'] = Trainer.objects.order_by('-xp')[:10]
        context['pokedex_leaders'] = Trainer.objects.order_by('-pokedex_number')[:10]
        context['catch_leaders'] = Trainer.objects.order_by('-pokemon_caught')[:10]
        context['spin_leaders'] = Trainer.objects.order_by('-pokestops_spun')[:10]
        context['walking_leaders'] = Trainer.objects.order_by('-kilometers_walked')[:10]
        context['battle_leaders'] = Trainer.objects.order_by('-battles_won')[:10]
        context['charts'] = self.get_charts()
        return context

    def chart_aggregate(self, team):
        return Trainer.objects.filter(team=team).aggregate(
            players=Count('pk'),
            team_xp=Sum('xp'),
            team_pokemon=Sum('pokemon_caught'),
            team_pokestops=Sum('pokestops_spun'),
            team_kilometers=Sum('kilometers_walked'),
            team_battles=Sum('battles_won'),
        )

    def get_charts(self):
        mystic = self.chart_aggregate(MYSTIC)
        valor = self.chart_aggregate(VALOR)
        instinct = self.chart_aggregate(INSTINCT)
        charts = {}
        for datum in ['players', 'team_xp', 'team_pokemon', 'team_pokestops',
                      'team_kilometers', 'team_battles']:
            charts[datum] = {
                'labels': ['Mystic', 'Valor', 'Instinct'],
                'datasets': [{
                    'label': datum,
                    'data': [int(mystic[datum]), int(valor[datum]), int(instinct[datum])],
                    'backgroundColor': ['#337ab7', '#d9534f',  '#f0ad4e'],
                }]
            }
        return charts


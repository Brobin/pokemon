from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Avg, Sum
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from .trainers.models import Trainer


class StatsView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['stats'] = Trainer.objects.aggregate(
            avg_xp=Avg('xp'),
            sum_xp=Sum('xp'),
            avg_pokemon_caught=Avg('pokemon_caught'),
            sum_pokemon_caught=Sum('pokemon_caught'),
            avg_battles_won=Avg('battles_won'),
            avg_pokestops_spun=Avg('pokestops_spun'),
            sum_pokestops_spun=Sum('pokestops_spun'),
            avg_pokedex_number=Avg('pokedex_number'),
        )
        context['xp_leaders'] = Trainer.objects.order_by('-xp')[:10]
        context['pokedex_leaders'] = Trainer.objects.order_by('-pokedex_number')[:10]
        context['catch_leaders'] = Trainer.objects.order_by('-pokemon_caught')[:10]
        context['spin_leaders'] = Trainer.objects.order_by('-pokestops_spun')[:10]
        return context

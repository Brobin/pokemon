from django import forms
from django.forms import inlineformset_factory

from .models import FavoritePokemon, Trainer


class TrainerForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    class Meta:
        model = Trainer
        fields = ['username', 'team', 'xp', 'pokemon_caught', 'pokestops_spun',
                  'battles_won', 'kilometers_walked', 'pokedex_number']


PokemonForm = inlineformset_factory(
    Trainer, FavoritePokemon,
    fields=['number', 'cp', 'shiny', 'attack', 'defense',
            'hp', 'fast_move', 'charge_move'],
    extra=8, min_num=0, max_num=8, can_delete=True)

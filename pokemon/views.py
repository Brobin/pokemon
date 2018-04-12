from django.db.models import Avg, Sum, Count
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
            sum_berries_fed=Sum('berries_fed'),
            avg_berries_fed=Avg('berries_fed'),
            sum_hours_defended=Sum('hours_defended'),
            avg_hours_defended=Avg('hours_defended'),
            sum_eggs_hatched=Sum('eggs_hatched'),
            avg_eggs_hatched=Avg('eggs_hatched'),
        )
        context['xp_leaders'] = Trainer.objects.order_by('-xp')[:5]
        context['pokedex_leaders'] = Trainer.objects.order_by('-pokedex_number', '-xp')[:5]
        context['catch_leaders'] = Trainer.objects.order_by('-pokemon_caught', '-xp')[:5]
        context['spin_leaders'] = Trainer.objects.order_by('-pokestops_spun', '-xp')[:5]
        context['walking_leaders'] = Trainer.objects.order_by('-kilometers_walked', '-xp')[:5]
        context['battle_leaders'] = Trainer.objects.order_by('-battles_won', '-xp')[:5]
        context['egg_leaders'] = Trainer.objects.order_by('-eggs_hatched', '-xp')[:5]
        context['defender_leaders'] = Trainer.objects.order_by('-hours_defended', '-xp')[:5]
        context['berry_leaders'] = Trainer.objects.order_by('-berries_fed', '-xp')[:5]
        context['charts']= self.get_charts()

        return context


    def get_charts(self):
        charts = {}
        for datum in ['xp', 'pokemon_caught', 'kilometers_walked', 'pokestops_spun',
            'battles_won', 'berries_fed', 'eggs_hatched', 'hours_defended']:
            mystic = Trainer.objects.exclude(**{datum + '__isnull': True}).filter(team=MYSTIC).aggregate(Avg(datum))
            valor = Trainer.objects.exclude(**{datum + '__isnull': True}).filter(team=VALOR).aggregate(Avg(datum))
            instinct = Trainer.objects.exclude(**{datum + '__isnull': True}).filter(team=INSTINCT).aggregate(Avg(datum))

            m, v, i = int(mystic[datum+'__avg'] or 0), int(valor[datum+'__avg'] or 0), int(instinct[datum+'__avg'] or 0)
            total = m + v + i

            charts[datum] = {
                'mystic': m,
                'valor': v,
                'instinct': i,
                'mystic_pct': 0 if total == 0 else m / total * 100,
                'valor_pct': 0 if total == 0 else v / total * 100,
                'instinct_pct': 0 if total == 0 else i / total * 100,
            }

        mystic = Trainer.objects.filter(team=MYSTIC).count()
        valor = Trainer.objects.filter(team=VALOR).count()
        instinct = Trainer.objects.filter(team=INSTINCT).count()
        total = mystic + valor + instinct

        charts['players'] = {
            'mystic': mystic,
            'valor': valor,
            'instinct': instinct,
            'mystic_pct': 0 if total == 0 else mystic / total * 100,
            'valor_pct': 0 if total == 0 else valor / total * 100,
            'instinct_pct': 0 if total == 0 else instinct / total * 100,
        }
        return charts


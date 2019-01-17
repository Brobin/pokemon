from django.core.cache import cache
from django.shortcuts import render

from django.views.generic import TemplateView

from math import floor

from .constants import CPM, BASE_STATS


POKEMON = {p['name']: p for p in BASE_STATS}


class PvPStatView(TemplateView):
    template_name = 'pvp/iv.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        pokemon = self.request.GET.get('pokemon', 'Skarmory')
        max_cp = int(self.request.GET.get('max_cp', 1500))

        context['choices'] = [p['name'] for p in BASE_STATS]
        context['choices'].sort()
        context['pokemon'] = pokemon
        context['max_cp'] = max_cp
        context['att_iv'] = int(self.request.GET.get('att_iv', 0))
        context['def_iv'] = int(self.request.GET.get('def_iv', 15))
        context['hp_iv'] = int(self.request.GET.get('hp_iv', 15))
        context['ivs'] = range(0, 16)

        key = pokemon + str(max_cp)
        combos = cache.get(key)
        if not combos:
            combos = list(self.get_combos(pokemon, max_cp))
            cache.set(key, combos, 60*60*24*7)

        context['combos'] = combos

        context['my_combo'] = self.get_my_combo(
            pokemon, context['att_iv'], context['def_iv'],
            context['hp_iv'], max_cp, combos[0][-2])
        return context

    def get_my_combo(self, name, at, de, hp, max_cp, max_product):
        base = POKEMON[name]
        for level in reversed(range(20, 81)):
            cp, product = self.calc_cp_and_product(base, level / 2.0, at, de, hp)
            if cp <= max_cp:
                return (level/2.0, at, de, hp, cp, product, floor(product/max_product*10000)/100)

    def get_combos(self, name, max_cp):
        base = POKEMON[name]
        combo = (base, 40, 15, 15, 15)
        cp, product = self.calc_cp_and_product(*combo)
        if cp <= max_cp:
            yield (40, 15, 15, 15, cp, product, 100)
            return

        combos = []
        for hp in reversed(range(0, 16)):
            for de in reversed(range(0, 16)):
                for at in range(0, 16):
                    for level in reversed(range(20, 81)):
                        cp, product = self.calc_cp_and_product(base, level / 2.0, at, de, hp)
                        if cp <= max_cp:
                            combos.append((level/2.0, at, de, hp, cp, product))
                            break
        combos.sort(key=lambda x: x[-1], reverse=True)
        c = combos[0]
        _max = c[-1]
        for c in combos[0:50]:
            yield c + (floor(c[-1]/_max*10000)/100,)

    def calc_cp_and_product(self, base, level, atk_iv, def_iv, hp_iv):
        _cpm = CPM[level]
        hp = (hp_iv + base['hp']) * _cpm
        attack = (atk_iv + base['attack']) * _cpm
        defense = (def_iv + base['defense']) * _cpm
        cp = max(floor(hp**0.5 * attack * defense**0.5 / 10), 10)
        stat_product = hp * defense * attack
        return cp, floor(stat_product)


class PvPTeamView(TemplateView):
    template_name = 'pvp/team.html'

from django.shortcuts import render

from django.views.generic import TemplateView

from math import floor

from .constants import CPM, BASE_STATS


class PvPStatView(TemplateView):
    template_name = 'pvp/iv.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        pokemon = self.request.GET.get('pokemon', 'Skarmory')
        max_cp = int(self.request.GET.get('max_cp', 1500))
        context['pokemon'] = pokemon
        context['max_cp'] = max_cp
        combos = list(self.get_combos(pokemon, max_cp))
        context['combos'] = combos
        context['choices'] = [p['name'] for p in BASE_STATS]
        return context

    def get_combos(self, name, max_cp):
        POKEMON = {p['name']: p for p in BASE_STATS}
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

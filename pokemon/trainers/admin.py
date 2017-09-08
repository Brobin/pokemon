from django.contrib import admin

from .models import Badge, FavoritePokemon, Trainer, TrainerBadge


class PokemonInline(admin.TabularInline):
    model = FavoritePokemon
    extra = 0
    min_num = 0
    max_num = 8


class TrainerBadgeInline(admin.TabularInline):
    model = TrainerBadge
    extra = 0


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    list_display_linke = ['name']


@admin.register(Trainer)
class TrainerAdmin(admin.ModelAdmin):
    list_display = ['username', 'level', 'xp', 'pokemon_caught']
    list_display_link = ['username']
    inlines = [PokemonInline, TrainerBadgeInline]

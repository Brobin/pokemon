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
    search_fields = ['name', 'description']


@admin.register(Trainer)
class TrainerAdmin(admin.ModelAdmin):
    list_display = ['username', 'xp', 'pokemon_caught', 'updated_at']
    list_display_link = ['username']
    list_filter = ['updated_at']
    search_fields = ['username']
    inlines = [PokemonInline, TrainerBadgeInline]

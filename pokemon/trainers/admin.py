from django.contrib import admin, messages
from django.forms import BaseInlineFormSet
from django.shortcuts import redirect

from .models import (
    Badge,
    BadgeApplication,
    FavoritePokemon,
    Trainer,
    TrainerBadge,
    TrainerUpdate,
)


class PokemonInline(admin.TabularInline):
    model = FavoritePokemon
    extra = 0
    min_num = 0
    max_num = 8
    classes = ['collapse']


class TrainerBadgeInline(admin.TabularInline):
    model = TrainerBadge
    extra = 0
    raw_id_fields = ['trainer']
    classes = ['collapse']


class TrainerUpdateFormset(BaseInlineFormSet):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs["instance"]
        self.queryset = TrainerUpdate.objects.filter(trainer=instance).order_by('-created_at')[:10]


class TrainerUpdateInline(admin.TabularInline):
    model = TrainerUpdate
    formset = TrainerUpdateFormset
    extra = 0
    raw_id_fields = ['trainer']
    classes = ['collapse']


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    list_display_linke = ['name']
    search_fields = ['name', 'description']
    inlines = [TrainerBadgeInline]


@admin.register(BadgeApplication)
class BadgeApplicationAdmin(admin.ModelAdmin):
    list_display = ['trainer', 'badge', 'approved', 'screenshot', 'screenshot2']
    list_display_links = ['trainer', 'badge', 'approved']
    actions = ['approve']
    list_filter = ['approved']

    def approve(self, request, queryset):
        for badge in queryset.filter(approved=False):
            badge.approve()
        messages.success(request, '{0} Badges approved'.format(queryset.count()))
        return redirect(request.path)


@admin.register(Trainer)
class TrainerAdmin(admin.ModelAdmin):
    list_display = ['username', 'xp', 'pokemon_caught', 'updated_at']
    list_display_link = ['username']
    list_filter = ['updated_at']
    search_fields = ['username', 'user__username']
    ordering = ['-updated_at']
    inlines = [PokemonInline, TrainerBadgeInline, TrainerUpdateInline]

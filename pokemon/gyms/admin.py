from django.contrib import admin

from .models import GymLog


@admin.register(GymLog)
class GymLogAdmin(admin.ModelAdmin):
    list_display = ['created_at', 'mystic', 'valor', 'instinct']
    list_display_links = ['created_at']
    ordering = ['-created_at']
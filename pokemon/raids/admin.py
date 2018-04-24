from django.contrib import admin

from .models import Raid, RaidRecord


@admin.register(Raid)
class RaidAdmin(admin.ModelAdmin):
    list_display = ['pokemon', 'tier', 'active']
    list_filter = ['active', 'tier']


@admin.register(RaidRecord)
class RaidRecordAdmin(admin.ModelAdmin):
    list_display = ['raid', 'trainer', 'time_remaining', 'verified', 'lineup_screenshot', 'finish_screenshot']
    list_display_links = ['raid', 'trainer']
    list_filter = ['verified', 'date']

from django.contrib import admin

from .models import IceProduction


@admin.register(IceProduction)
class IceProductionAdmin(admin.ModelAdmin):
    list_display = ('ice_type', 'topic', 'weight', 'date', 'hour')
    list_filter = ('ice_type', 'topic', 'weight', 'date')
    search_fields = ('ice_type', 'topic', 'weight', 'date', 'hour')

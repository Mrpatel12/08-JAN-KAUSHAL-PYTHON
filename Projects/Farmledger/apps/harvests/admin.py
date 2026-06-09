from django.contrib import admin
from .models import Harvest


@admin.register(Harvest)
class HarvestAdmin(admin.ModelAdmin):
    list_display = ('id', 'farm', 'harvested_at', 'quantity', 'unit')
    list_filter = ('harvested_at',)
    search_fields = ('farm__name', 'notes')

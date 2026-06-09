from django.contrib import admin
from .models import Crop


@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    list_display = ('name', 'farm', 'status', 'planted_at')
    search_fields = ('name', 'variety', 'farm__name')
    list_filter = ('status',)

from django.contrib import admin
from .models import Farm


@admin.register(Farm)
class FarmAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'acreage', 'status')
    search_fields = ('name', 'owner__email')
    list_filter = ('status',)

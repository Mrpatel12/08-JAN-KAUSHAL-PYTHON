from django.contrib import admin
from .models import Expense


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('id', 'farm', 'amount', 'currency', 'occurred_at')
    list_filter = ('currency', 'occurred_at')
    search_fields = ('farm__name', 'notes')

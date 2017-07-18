from django.contrib import admin
from .models import Credit


@admin.register(Credit)
class CreditAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Credit', {'fields': ('point',)}),
    )
    list_display = ['user', 'point']

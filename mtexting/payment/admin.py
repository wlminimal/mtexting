from django.contrib import admin
from .models import StripeAccount


@admin.register(StripeAccount)
class StripeAccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'stripe_id', 'created_at', 'modifed')
    readonly_fields = ('stripe_id', )

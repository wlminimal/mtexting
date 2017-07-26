from django import forms
from django.contrib import admin
from django.contrib import messages
from django.conf import settings

from .models import Credit, Plan
import stripe


@admin.register(Credit)
class CreditAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Credit', {'fields': ('point',)}),
    )
    list_display = ['user', 'point', ]


class PlanCreationForm(forms.ModelForm):

    # Validate if plan id already exists
    def clean_plan_id(self):
        stripe.api_key = settings.STRIPE_PRIVATE_TOKEN

        plan_id = self.cleaned_data['plan_id']
        try:
            plan = stripe.Plan.retrieve(plan_id)
        except stripe.InvalidRequestError as e:
            return plan_id
        raise forms.ValidationError("Duplicate Plan Id, Choose the other.")

    class Meta:
        model = Plan
        fields = ('name', 'plan_id', 'amount', 'currency', 'interval')


class PlanChangeForm(forms.ModelForm):
    # Only editable name field
    class Meta:
        model = Plan
        fields = ('name', )


def delete_plan_actions(modeladmin, request, queryset):
    stripe.api_key = settings.STRIPE_PRIVATE_TOKEN
    for obj in queryset:
        plan = stripe.Plan.retrieve(obj.plan_id)
        plan.delete()
    queryset.delete()


delete_plan_actions.short_description = "Mark selected plan for delete"


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'plan_id', 'amount', 'currency', 'interval')
    actions = [delete_plan_actions]

    def get_form(self, request, obj=None, **kwargs):
        if obj:  # obj is not None, so this is a change page
            kwargs['form'] = PlanChangeForm
        else:  # obj is None, so this is an add page
            kwargs['form'] = PlanCreationForm
        return super(PlanAdmin, self).get_form(request, obj, **kwargs)

    def save_model(self, request, obj, form, change):
        # Save Plan object to Stripe
        # make sure there is no duplicate plan

        stripe.api_key = settings.STRIPE_PRIVATE_TOKEN
        plans = stripe.Plan.list()
        plan_exists = False

        for plan in plans.data:
            if plan.id == obj.plan_id:
                plan_exists = True

        if plan_exists:
            # messages.add_message(request, messages.error, "Plan already exists")
            # Updating Plan info
            plan = stripe.Plan.retrieve(obj.plan_id)
            plan.name = obj.name
            plan.save()

        else:
            # Create a plan
            stripe.Plan.create(
                name=obj.name,
                id=obj.plan_id,
                amount=obj.amount,
                currency=obj.currency,
                interval=obj.interval
            )

        super(PlanAdmin, self).save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        # Delete Plan object from Stripe
        stripe.api_key = settings.STRIPE_PRIVATE_TOKEN
        plan = stripe.Plan.retrieve(obj.plan_id)
        plan.delete()
        super(PlanAdmin, self).delete_model(request, obj)

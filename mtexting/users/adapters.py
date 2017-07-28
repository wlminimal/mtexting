from django.conf import settings
from mtexting.payment.models import StripeAccount
from plan.models import Plan

from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.utils import user_username, user_email, user_field
from twilio.rest import Client
import stripe


class AccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        return getattr(settings, 'ACCOUNT_ALLOW_REGISTRATION', True)

    def save_user(self, request, user, form, commit=True):
        data = form.cleaned_data
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        username = data.get('username')
        user_email(user, email)
        user_username(user, username)
        if first_name:
            user_field(user, 'first_name', first_name)
        if last_name:
            user_field(user, 'last_name', last_name)
        if 'password1' in data:
            user.set_password(data["password1"])
        else:
            user.set_unusable_password()
        self.populate_username(request, user)

        # make a twilio sub account
        account_sid = getattr(settings, 'TWILIO_ACCOUNT_SID')
        auth_token = getattr(settings, 'TWILIO_AUTH_TOKEN')

        client = Client(account_sid, auth_token)

        # Twilio sub account
        # TODO : Check duplicate friendly_name in twilio account,
        # if there is a dupulicate name, add random number
        # at the end of friendly_name.
        # account = client.api.accounts.create(friendly_name=user.username)
        # user.account_sid = account.sid
        # user.account_name = account.friendly_name

        # Create a STRIPE account
        stripe.api_key = settings.STRIPE_PRIVATE_TOKEN
        customer = stripe.Customer.create(email=user.email)

        user.stripe_id = customer.id
        user.credit = 200  # Free creidt at signup
        # Subscribe to Free plan
        free_plan_id = 'free'
        free_plan = Plan.objects.get(plan_id=free_plan_id)

        stripe.Subscription.create(
            customer=customer.id,
            plan=free_plan_id
        )

        user.plan = free_plan

        if commit:
            user.save()

        stripe_account = StripeAccount.objects.create(user=user,
                                                      stripe_id=customer.id)

        return user


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_open_for_signup(self, request, sociallogin):
        return getattr(settings, 'ACCOUNT_ALLOW_REGISTRATION', True)

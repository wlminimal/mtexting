from django.conf import settings
from plan.models import Credit
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.utils import user_username, user_email, user_field
from twilio.rest import Client


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
        account = client.api.accounts.create(friendly_name=user.username)
        user.account_sid = account.sid
        user.account_name = account.friendly_name

        if commit:
            user.save()

        credit = Credit.objects.create(user=user)

        return user


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_open_for_signup(self, request, sociallogin):
        return getattr(settings, 'ACCOUNT_ALLOW_REGISTRATION', True)

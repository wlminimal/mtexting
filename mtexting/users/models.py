from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.core.validators import RegexValidator
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from plan.models import Plan


@python_2_unicode_compatible
class User(AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = models.CharField(_('Name of User'), blank=True, max_length=255)
    company_name = models.CharField(_('Company Name'), blank=True, max_length=255)
    mobile_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                  message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    mobile_number = models.CharField(_('Mobile Number'), blank=True,
                                    validators=[mobile_regex]
                                    , max_length=15)
    # TODO: Make a Twillio User object separately
    account_sid = models.CharField(_('Account SID'), blank=True, max_length=255, default="twilio_sid")
    account_name = models.CharField(_('Account Name'), blank=True, max_length=255, default="account name")
    credit = models.IntegerField(default=0)
    plan = models.ForeignKey(
        Plan,
        on_delete=models.CASCADE,
        related_name='subscriber',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})

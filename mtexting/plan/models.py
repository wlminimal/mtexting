from django.db import models
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Credit(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
    )
    point = models.IntegerField(default=200)
    fisttime_user = models.BooleanField(default=False)


class Plan(models.Model):
    name = models.CharField(max_length=255)
    plan_id = models.CharField(max_length=255,
                               help_text="A Unique ID for this plan, which will be\
                                          used throughtout the API.")
    amount = models.IntegerField(default=2000)
    currency = models.CharField(max_length=255, default="usd")
    interval = models.CharField(max_length=255, default="month")

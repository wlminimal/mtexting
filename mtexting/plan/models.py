from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Credit(models.Model):
    credit = models.IntegerField(default=200)

    def __str__(self):
        return self.credit + " credits"


class Plan(models.Model):
    name = models.CharField(max_length=255)
    plan_id = models.CharField(max_length=255,
                               help_text="A Unique ID for this plan, which will be\
                                          used throughtout the API.")
    amount = models.IntegerField(default=2000)
    currency = models.CharField(max_length=255, default="usd")
    interval = models.CharField(max_length=255, default="month")
    credit = models.ForeignKey(
        Credit,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='+',
    )

    def __str__(self):
        return self.name

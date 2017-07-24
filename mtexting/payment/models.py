from django.db import models
from django.conf import settings
import stripe


class StripeObject(models.Model):
    stripe_id = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modifed = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class StripeAccount(StripeObject):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                null=True,
                                related_name='stripe_customer')

    @property
    def stripe_customer(self):
        return stripe.Customer.retrieve(self.stripe_id)

    def __str__(self):
        return str(self.user)

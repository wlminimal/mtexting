from django.conf import settings

import stripe


def set_stripe_key(key):
    stripe.api_key = key
    return stripe


def create_charge(amount, description, customer=None, currency="usd", source=None):
    stripe = set_stripe_key(settings.STRIPE_PRIVATE_TOKEN)

    if customer is not None:
        charge = stripe.Charge.create(
            amount=amount,
            description=description,
            customer=customer,
            currency=currency,
        )
    else:
        charge = stripe.Charge.create(
            amount=amount,
            description=description,
            source=source,
            currency=currency,
        )

from django.shortcuts import render
from django.conf import settings

import stripe


def checkout(request):
    public_key = settings.STRIPE_PUBLIC_TOKEN
    stripe.api_key = settings.STRIPE_PRIVATE_TOKEN

    if request.method == 'POST':
        token = request.POST.get('stripeToken')

        try:
            charge = stripe.charge.create(
                amount=5000,
                description="mTexting",
                source=token,
                currency="usd"
            )
        except stripe.error.CardError as e:
            # Since it's a decline, stripe.error.CardError will be caught
            body = e.json_body
            err = body['error']
        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
          pass
        except stripe.error.InvalidRequestError as e:
          # Invalid parameters were supplied to Stripe's API
          pass
        except stripe.error.AuthenticationError as e:
          # Authentication with Stripe's API failed
          # (maybe you changed API keys recently)
          pass
        except stripe.error.APIConnectionError as e:
          # Network communication with Stripe failed
          pass
        except stripe.error.StripeError as e:
          # Display a very generic error to the user, and maybe send
          # yourself an email
          pass
        except Exception as e:
          # Something else happened, completely unrelated to Stripe
          pass

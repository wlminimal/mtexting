from django.shortcuts import render
from django.conf import settings
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import StripeAccount

import stripe


@login_required
def checkout(request):
    public_key = settings.STRIPE_PUBLIC_TOKEN
    stripe.api_key = settings.STRIPE_PRIVATE_TOKEN

    if request.method == 'POST':
        token = request.POST.get('stripeToken')
        user = request.user
        amount = request.POST.get('amount')
        # Must return stripe customer id
        stripe_customer = user.stripe_customer.stripe_customer
        if stripe_customer.source is not None:
            # user has a card info?

            charge = stripe.Charge.create(
                amount=amount,
                description="mTexting",
                customer=stripe_customer,
                currency="usd"
            )
<<<<<<< HEAD
        except stripe.error.CardError as e:
            # Since it's a decline, stripe.error.CardError will be caught
            body = e.json_body
            err = body['error']
        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly

        except stripe.error.InvalidRequestError as e:
          # Invalid parameters were supplied to Stripe's API

        except stripe.error.AuthenticationError as e:
          # Authentication with Stripe's API failed
          # (maybe you changed API keys recently)

        except stripe.error.APIConnectionError as e:
          # Network communication with Stripe failed

        except stripe.error.StripeError as e:
          # Display a very generic error to the user, and maybe send
          # yourself an email

        except Exception as e:
          # Something else happened, completely unrelated to Stripe
=======
            return HttpResponseRedirect(reverse('thank-you'))
        else:
            # First time payment
            stripe_customer.source = token
            # Charge using new customer.id
            charge = stripe.Charge.create(
                amount=amount,
                description=str(amount),
                source=stripe_customer.id,
                currency="usd"
            )

            return HttpResponseRedirect(reverse('thank-you'))

        # Send Email?


        # Comment out for testing purpose

        # try:
        #     charge = stripe.charge.create(
        #         amount=5000,
        #         description="mTexting",
        #         source=token,
        #         currency="usd"
        #     )
        #     # Send Email?
        #
        #     return HttpResponseRedirect(reverse('thank-you'))
        #
        # except stripe.error.CardError as e:
        #     # Since it's a decline, stripe.error.CardError will be caught
        #     body = e.json_body
        #     err = body['error']
        #
        #     return HttpResponseRedirect(reverse('declined'))
        # except stripe.error.RateLimitError as e:
        #     # Too many requests made to the API too quickly
        #     return HttpResponseRedirect(reverse('payment-error'))
        # except stripe.error.InvalidRequestError as e:
        #     # Invalid parameters were supplied to Stripe's API
        #     return HttpResponseRedirect(reverse('payment-error'))
        # except stripe.error.AuthenticationError as e:
        #     # Authentication with Stripe's API failed
        #     # (maybe you changed API keys recently)
        #     return HttpResponseRedirect(reverse('payment-error'))
        # except stripe.error.APIConnectionError as e:
        #     # Network communication with Stripe failed
        #     return HttpResponseRedirect(reverse('payment-error'))
        # except stripe.error.StripeError as e:
        #     # Display a very generic error to the user, and maybe send
        #     # yourself an email
        #     return HttpResponseRedirect(reverse('payment-error'))
        # except Exception as e:
        #     # Something else happened, completely unrelated to Stripe
        #     return HttpResponseRedirect(reverse('payment-error'))
    else:
        return render(request, 'payment/checkout.html', {'public_key': public_key})
>>>>>>> 9b0797bd88ec6e5c6c0e218cbf4030dac3925845

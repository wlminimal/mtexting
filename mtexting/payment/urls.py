from django.conf.urls import url
from django.views.generic import TemplateView

from .views import checkout


urlpatterns = [
    url(r'^checkout/', checkout, name="checkout"),
    url(r'^thank-you/$', TemplateView.as_view(template_name="payment/thank-you.html"), name="thank-you"),
    url(r'^declined/$', TemplateView.as_view(template_name="payment/declined.html"), name="declined"),
    url(r'^payment-error/$', TemplateView.as_view(template_name="payment/payment-error.html"), name="payment-error"),
]

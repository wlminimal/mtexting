from django.conf.urls import url
from django.views.generic import TemplateView


urlpatterns = [
    url(r'^upgrade-plan/',
        TemplateView.as_view(
            template_name="plan/upgrade-plan.html"),
        name="upgrade-plan"),
]

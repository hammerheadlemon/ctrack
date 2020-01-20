from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView

from .models import Organisation


class OrganisationDetailView(LoginRequiredMixin, DetailView):
    model = Organisation

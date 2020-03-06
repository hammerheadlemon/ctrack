from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
#from django.http import HttpRequest
#from django.http import HttpResponse
from django.views.generic import DetailView
from typing import Dict

from .models import Organisation


class OrganisationDetailView(LoginRequiredMixin, DetailView):
    model = Organisation

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data()
        org = kwargs['object']
        no_addr = org.addresses.count()
        if no_addr > 1:
            context['no_addr'] = no_addr
            addr = org.addresses.all()
            context['addr'] = addr
        else:
            context['no_addr'] = 1
            addr = org.addresses.first()
            context['addr'] = addr
        people = org.person_set.all()
        context['people'] = people
        return context

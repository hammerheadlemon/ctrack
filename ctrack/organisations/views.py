from typing import Any
from typing import Dict

from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import DetailView, ListView, CreateView

from .forms import OrganisationCreateForm, AddressCreateForm
from .models import Organisation, Address


def create_org_with_address(request):
    OrgCreateInlineFormSet = inlineformset_factory(Organisation, Address, exclude=(), can_delete=False, form=AddressCreateForm, extra=3)
    if request.method == "POST":
        formset = OrgCreateInlineFormSet(request.POST)
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect("/")
    else:
        formset = OrgCreateInlineFormSet()
    return render(request, "organisations/org_create_formset.html", {"formset": formset})


class OrganisationCreate(LoginRequiredMixin, CreateView):
    form_class = OrganisationCreateForm
    model = Organisation
    template_name = "organisations/organisation_create.html"


class OrganisationListView(LoginRequiredMixin, ListView):
    model = Organisation

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["organisation_list"] = Organisation.objects.all().order_by("name")
        return context


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
        applicable_systems = org.applicablesystem_set.all()
        context['applicable_systems'] = applicable_systems
        return context

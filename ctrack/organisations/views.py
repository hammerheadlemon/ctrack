from typing import Any, Dict

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db import transaction
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, FormView, ListView

from .forms import AddressInlineFormSet, IncidentReportForm, OrganisationCreateForm
from .models import IncidentReport, Organisation, Person


class PersonListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Person
    template_name = "organisations/person_list.html"
    permission_required = "organisations.view_person"


class OrganisationCreate(LoginRequiredMixin, CreateView):
    model = Organisation
    template_name = "organisations/org_create_formset.html"
    form_class = OrganisationCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["addresses"] = AddressInlineFormSet(self.request.POST)
        else:
            context["addresses"] = AddressInlineFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        addresses = context["addresses"]
        with transaction.atomic():
            #            form.instance.updated_by = self.request.user REMOVED updated_by
            self.object = form.save()
            if addresses.is_valid():
                addresses.instance = self.object
                addresses.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("organisations:detail", kwargs={"slug": self.object.slug})


class OrganisationListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Organisation
    permission_required = "organisations.view_organisation"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["organisation_list"] = Organisation.objects.all().order_by("name")
        return context


class OrganisationDetailView(LoginRequiredMixin, DetailView):
    model = Organisation

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data()
        org = kwargs["object"]
        no_addr = org.addresses.count()
        if no_addr > 1:
            context["no_addr"] = no_addr
            addr = org.addresses.all()
            context["addr"] = addr
        else:
            context["no_addr"] = 1
            addr = org.addresses.first()
            context["addr"] = addr
        people = org.person_set.all()
        context["people"] = people
        applicable_systems = org.applicablesystem_set.all()
        context["applicable_systems"] = applicable_systems
        return context


class IncidentReportCreateView(LoginRequiredMixin, FormView):
    model = IncidentReport
    form_class = IncidentReportForm
    template_name = "organisations/incidentreport_form.html"
    success_url = reverse_lazy("core:home")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["org"] = self.request.user.stakeholder.person.organisation
        kwargs["reporting_person"] = self.request.user.stakeholder.person
        return kwargs

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse("core:home"))

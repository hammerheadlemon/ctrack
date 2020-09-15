from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, FormView, ListView

from ctrack.caf.models import EssentialService, CAF
from ctrack.register.models import EngagementEvent
from .forms import AddressInlineFormSet, IncidentReportForm, OrganisationCreateForm
from .models import IncidentReport, Organisation, Person


# TODO - needs a permission on this view
def essential_service_detail(request, pk):
    es = EssentialService.objects.get(pk=pk)
    org = es.organisation
    cafs = CAF.objects.filter(organisation=org.pk)
    asses = es.systems.all()
    # es = get_object_or_404(EssentialService, organisation__pk=org_pk)
    context = {"es": es, "asses": asses, "cafs": cafs}
    return render(request, "organisations/essential_service_detail.html", context)


class PersonListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Person
    template_name = "organisations/person_list.html"
    permission_required = "organisations.view_person"


def person_detail(request, person_id):
    p = get_object_or_404(Person, pk=person_id)
    return render(request, "organisations/person_detail.html", {"person": p})


class OrganisationCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Organisation
    template_name = "organisations/org_create_formset.html"
    form_class = OrganisationCreateForm
    permission_required = "organisations.add_organisation"

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


class OrganisationDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Organisation
    permission_required = "organisations.view_organisation"

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data()
        org = kwargs["object"]
        peoples = org.person_set.all()
        engagement_events = EngagementEvent.objects.filter(participants__in=peoples)
        essential_services = EssentialService.objects.filter(organisation=org)
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
        applicable_systems = org.applicable_systems()
        context["applicable_systems"] = applicable_systems
        context["engagement_events"] = engagement_events
        context["essential_services"] = essential_services
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

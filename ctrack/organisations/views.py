import itertools
from typing import Any

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, FormView, ListView

from ctrack.caf.models import CAF, EssentialService
from ctrack.register.models import EngagementEvent, NoteEvent, SingleDateTimeEvent
from .forms import AddressInlineFormSet, IncidentReportForm, OrganisationCreateForm
from .models import IncidentReport, Organisation, Person
from .utils import filter_private_events


# TODO - needs a permission on this view
def essential_service_detail(request, pk):
    es = EssentialService.objects.get(pk=pk)
    org = es.organisation
    cafs = CAF.objects.filter(organisation=org.pk)
    asses = es.systems.all()
    # es = get_object_or_404(EssentialService, organisation__pk=org_pk)
    context = {"es": es, "asses": asses, "cafs": cafs}
    return render(request, "organisations/essential_service_detail.html", context)


def person_contact_history(request, person_id):
    events = SingleDateTimeEvent.objects.filter(participants__id=person_id).order_by(
        "-date"
    )
    person = get_object_or_404(Person, id=person_id)

    filtered_out_private = [
        filter_private_events(
            person.get_single_datetime_events(), request.user
        )
    ]
    all_events = list(itertools.chain.from_iterable(filtered_out_private))
    sorted_events = sorted(all_events, key=lambda e: e.date, reverse=True)

    return render(
        request,
        "organisations/contact_history.html",
        {"events": sorted_events, "person": person},
    )


class OrganisationListViewByLeadInspector(ListView):
    model = Organisation
    template_name = "organisations/organisation_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        inspector = get_user_model().objects.get(id=self.kwargs.get("id"))
        context["organisation_list"] = Organisation.objects.filter(
            lead_inspector=inspector, oes=True
        )
        context["inspector"] = inspector
        context["is_oes"] = True
        return context


class PersonListView(PermissionRequiredMixin, ListView):
    model = Person
    template_name = "organisations/person_list.html"
    permission_required = "organisations.view_person"


def person_detail(request, person_id):
    p = get_object_or_404(Person, pk=person_id)
    return render(request, "organisations/person_detail.html", {"person": p})


def oes_list(request):
    oes = Organisation.objects.filter(oes=True)
    return render(
        request,
        "organisations/organisation_list.html",
        {"organisation_list": oes, "is_oes": True},
    )


class OrganisationCreate(PermissionRequiredMixin, CreateView):
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


class OrganisationListView(PermissionRequiredMixin, ListView):
    model = Organisation
    permission_required = "organisations.view_organisation"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["organisation_list"] = Organisation.objects.all().order_by("name")
        return context


class OrganisationDetailView(PermissionRequiredMixin, DetailView):
    model = Organisation
    permission_required = "organisations.view_organisation"

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data()
        org = kwargs["object"]
        peoples = org.person_set.all()
        cafs = org.caf_set.all()

        # simple datetime events for org
        notes = NoteEvent.objects.filter(
            user=self.request.user, organisation=self.object
        ).order_by("-created_date")
        filtered_out_private = [
            filter_private_events(
                person.get_single_datetime_events(), self.request.user
            )
            for person in peoples
        ]
        all_events = list(itertools.chain.from_iterable(filtered_out_private))
        all_events = set(all_events)
        sorted_events = sorted(all_events, key=lambda e: e.date, reverse=True)
        for x in sorted_events:
            if isinstance(x, NoteEvent):
                delattr(x, "date")

        # Some events will not involve a participant, which is what ties an event to an organisation.
        # Because we want to list events to an organisation here we must related it via the CAF object too...
        engagement_events = EngagementEvent.objects.filter(
            Q(participants__in=peoples) | Q(related_caf__in=cafs)
        ).order_by("-date")
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
        context["notes"] = notes
        context["applicable_systems"] = applicable_systems
        context["engagement_events"] = engagement_events
        context["essential_services"] = essential_services
        context["cafs"] = cafs
        context["single_datetime_events"] = sorted_events
        return context


class IncidentReportCreateView(FormView):
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

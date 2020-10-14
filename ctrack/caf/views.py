from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, FormView, ListView

from ctrack.assessments.models import CAFAssessmentOutcomeScore
from ctrack.caf.forms import (
    ApplicableSystemCreateFromCafForm,
    ApplicableSystemCreateFromOrgForm,
)
from ctrack.caf.models import CAF, ApplicableSystem
from ctrack.organisations.models import Organisation


class ListCAF(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = CAF
    permission_required = "caf.view_caf"


# Let's write a traditional function view!
@login_required()
@permission_required("caf.view_caf")
def caf_detail_view(request, pk):
    caf = CAF.objects.get(pk=pk)
    # get any assessments that have been done on this caf
    assessments = caf.cafassessment_set.all()
    # caf_principles = CAFPrinciple.objects.all()
    _scrs = []
    for ass in assessments:
        lst_scores = [ass, CAFAssessmentOutcomeScore.objects.filter(caf_assessment=ass)]
        _scrs.append(lst_scores)
    context = {
        "object": caf,
        "assessments_and_scores": _scrs,
        "organisation": caf.organisation,
        "systems": caf.systems.all(),
        "single_date_events": caf.cafsingledateevent_set.all(),
        "twin_date_events": caf.caftwindateevent_set.all(),
    }
    return render(request, "caf/caf_detail.html", context)


class ListApplicableSystem(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = ApplicableSystem
    # apparently you can pass a list of model objects to a template if you name it
    # here - otherwise you need to provide a QuerySet
    template_name = "caf/applicablesystem_list.html"
    permission_required = "caf.view_caf"

    def get_queryset(self):
        ess = ApplicableSystem.objects.all().order_by("name")
        return ess

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ApplicableSystemDetail(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = ApplicableSystem
    template_name = "caf/applicablesystem_detail.html"
    permission_required = "caf.view_applicablesystem"


@login_required
@permission_required("caf.add_applicablesystem")
def applicable_system_create_from_caf(request, caf_id):
    org_id = CAF.objects.get(pk=caf_id).organisation().id
    caf = CAF.objects.get(id=caf_id)
    if request.method == "POST":
        form = ApplicableSystemCreateFromCafForm(
            request.POST, caf_id=caf_id, org_id=org_id
        )
        if form.is_valid():
            ApplicableSystem.objects.create(
                name=form.cleaned_data["name"],
                function=form.cleaned_data["function"],
                caf=form.cleaned_data["caf"],
                organisation=form.cleaned_data["organisation"],
            )
            return HttpResponseRedirect(reverse("caf:detail", args=[caf_id]))
    else:
        form = ApplicableSystemCreateFromCafForm(caf_id=caf_id, org_id=org_id)

    return render(
        request,
        "caf/applicable_system_create_from_caf.html",
        {"form": form, "caf": caf},
    )


class ApplicableSystemCreateFromOrg(
    LoginRequiredMixin, PermissionRequiredMixin, FormView
):
    form_class = ApplicableSystemCreateFromOrgForm
    template_name = "caf/applicable_system_create_from_org.html"
    permission_required = "caf.add_applicablesystem"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["organisation"] = Organisation.objects.get(slug=self.kwargs["slug"])
        return context

    def form_valid(self, form):
        ass = ApplicableSystem.objects.create(
            name=form.cleaned_data["name"],
            function=form.cleaned_data["function"],
            # organisation=form.cleaned_data["organisation"],
            # caf=form.cleaned_data["caf"],
        )
        es = form.cleaned_data["essential_service"]
        es.systems.add(ass)
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        org = Organisation.objects.get(slug=self.kwargs["slug"])
        asses = org.applicable_systems()
        # org_cafs = org.caf_set.all()
        kwargs["org_id"] = org.id
        kwargs["slug"] = org.slug
        kwargs["org_name"] = org.name
        # kwargs["org_cafs"] = list(org_cafs)
        return kwargs

    def get_success_url(self):
        return reverse_lazy("organisations:detail", args=[self.kwargs["slug"]])

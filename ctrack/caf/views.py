from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, FormView

from ctrack.assessments.models import CAFAssessmentOutcomeScore
from ctrack.caf.forms import ApplicableSystemCreateFromOrgForm, ApplicableSystemCreateFromCafForm
from ctrack.caf.models import ApplicableSystem, CAF
from ctrack.organisations.models import Organisation


class ListCAF(LoginRequiredMixin, ListView):
    model = CAF


# Let's write a traditional function view!
def caf_detail_view(request, pk):
    caf = CAF.objects.get(pk=pk)
    # get any assessments that have been done on this caf
    assessments = caf.cafassessment_set.all()
    # caf_principles = CAFPrinciple.objects.all()
    _scrs = []
    for ass in assessments:
        lst_scores = []
        lst_scores.append(ass)
        lst_scores.append(CAFAssessmentOutcomeScore.objects.filter(caf_assessment=ass))
        _scrs.append(lst_scores)
    context = {
        'object': caf,
        'assessments_and_scores': _scrs,
        'organisation': ApplicableSystem.objects.filter(caf=caf).first().organisation,
        'systems': caf.applicable_systems.all()
    }
    return render(request, 'caf/caf_detail.html', context)


class ListApplicableSystem(LoginRequiredMixin, ListView):
    model = ApplicableSystem
    # apparently you can pass a list of model objects to a template if you name it
    # here - otherwise you need to provide a QuerySet
    template_name = "caf/applicablesystem_list.html"

    def get_queryset(self):
        ess = ApplicableSystem.objects.all().order_by("organisation__name")
        return ess

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ApplicableSystemDetail(LoginRequiredMixin, DetailView):
    model = ApplicableSystem
    template_name = "caf/applicablesystem_detail.html"


def applicable_system_create_from_caf(request, caf_id):
    org_id = CAF.objects.get(pk=caf_id).organisation().id
    if request.method=="POST":
        form = ApplicableSystemCreateFromCafForm(request.POST, caf_id=caf_id, org_id=org_id)
        if form.is_valid():
            ApplicableSystem.objects.create(
                name=form.cleaned_data["name"],
                description=form.cleaned_data["description"],
                caf=form.cleaned_data["caf"],
                organisation=form.cleaned_data["organisation"]
            )
            return HttpResponseRedirect(reverse("caf:detail", args=[caf_id]))
    else:
        form = ApplicableSystemCreateFromCafForm(caf_id=caf_id, org_id=org_id)

    return render(request, "caf/applicable_system_create_from_caf.html", {"form": form})


class ApplicableSystemCreateFromOrg(LoginRequiredMixin, FormView):
    form_class = ApplicableSystemCreateFromOrgForm
    template_name = "caf/applicable_system_create_from_org.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["organisation"] = Organisation.objects.get(slug=self.kwargs["slug"])
        return context

    def form_valid(self, form):
        ass = ApplicableSystem.objects.create(
            name=form.cleaned_data["name"],
            description=form.cleaned_data["description"],
            organisation=form.cleaned_data["organisation"],
            caf=form.cleaned_data["caf"]
        )
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        org = Organisation.objects.get(slug=self.kwargs["slug"])
        asses = org.applicablesystem_set.all()
        org_cafs = {ass.caf for ass in asses}
        kwargs['org_id'] = org.id
        kwargs['slug'] = org.slug
        kwargs['org_name'] = org.name
        kwargs['org_cafs'] = list(org_cafs)
        return kwargs

    def get_success_url(self):
        return reverse_lazy("organisations:detail", args=[self.kwargs['slug']])

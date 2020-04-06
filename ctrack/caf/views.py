from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import CreateView, ListView, DetailView

from ctrack.assessments.models import CAFAssessment, CAFObjective, CAFPrinciple, CAFAssessmentOutcomeScore
from ctrack.caf.forms import CAFForm
from ctrack.caf.models import ApplicableSystem, CAF


class CreateCAF(LoginRequiredMixin, CreateView):
    form_class = CAFForm
    template_name = "caf/create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class
        return context


class ListCAF(LoginRequiredMixin, ListView):
    pass


# class DetailCAF(LoginRequiredMixin, DetailView):
#     model = CAF

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
        'organisation': ApplicableSystem.objects.filter(caf=caf).first().organisation
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

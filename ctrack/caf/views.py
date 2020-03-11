from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, DetailView

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


class DetailCAF(LoginRequiredMixin, DetailView):
    model = CAF


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

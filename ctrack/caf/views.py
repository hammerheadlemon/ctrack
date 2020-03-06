from django.views.generic import CreateView, ListView

from ctrack.caf.forms import CAFForm
from ctrack.caf.models import ApplicableSystem


class CreateCAF(CreateView):
    form_class = CAFForm
    template_name = "caf/create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class
        return context


class ListCAF(ListView):
    pass


class ListApplicableSystem(ListView):
    model = ApplicableSystem
    # apparently you can pass a list of model objects to a template if you name it
    # here - otherwise you need to provide a QuerySet
    template_name = "caf/applicablesystem_list.html"

    def get_queryset(self):
        # TODO sort this list using basic Python sorted()
        ess = ApplicableSystem.objects.with_primary_contact()  # returns a list, not a QuerySet
        return ess

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context



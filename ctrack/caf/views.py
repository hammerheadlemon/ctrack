from django.views.generic import CreateView, ListView

from ctrack.caf.forms import CAFForm
from ctrack.caf.models import EssentialService


class CreateCAF(CreateView):
    form_class = CAFForm
    template_name = "caf/create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class
        return context


class ListCAF(ListView):
    pass


class ListEssentialService(ListView):
    model = EssentialService

    # TODO - add primary_nis_contact tick to the context
    #    Context can be easily found with:
    #    org.person_set.filter(primary_nis_contact=True) or similar

    def get_queryset(self):
        ess = EssentialService.objects.all().order_by("organisation__name")
        return ess

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context



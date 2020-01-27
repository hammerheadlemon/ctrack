from django.views.generic import CreateView

from ctrack.caf.forms import CAFForm


class CreateCAF(CreateView):
    form_class = CAFForm
    template_name = "caf/create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class
        return context





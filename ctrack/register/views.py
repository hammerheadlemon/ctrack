from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView

from ctrack.organisations.models import Organisation
from ctrack.register.forms import EngagementEventCreateForm


class EngagementEventCreate(LoginRequiredMixin, FormView):
    fields = "__all__"
    form_class = EngagementEventCreateForm
    template_name = "register/engagementevent_form.html"
    success_url = reverse_lazy("organisations:list")

    def form_valid(self, form):
        ee = form.save(commit=False)
        ee.user = self.request.user
        form.save()
        return HttpResponseRedirect(reverse("organisations:list"))

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["org_slug"] = self.kwargs["slug"]
        kwargs["user"] = get_user_model()
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["org"] = Organisation.objects.get(slug=self.kwargs["slug"])
        return context

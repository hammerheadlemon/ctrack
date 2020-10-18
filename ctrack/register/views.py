from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import DeleteView, FormView

from ctrack.caf.models import CAF
from ctrack.organisations.models import Organisation
from ctrack.register.forms import CreateSimpleDateTimeEventForm, EngagementEventCreateForm
from ctrack.register.models import EngagementEvent


class EngagementEventDelete(DeleteView):
    model = EngagementEvent

    def get_success_url(self):
        return reverse_lazy("organisations:detail", args=[self.kwargs["slug"]])


class EngagementEventCreate(FormView):
    fields = "__all__"
    form_class = EngagementEventCreateForm
    template_name = "register/engagementevent_form.html"

    # success_url = reverse_lazy("organisations:list")

    def form_valid(self, form):
        ee = form.save(commit=False)
        ee.user = self.request.user
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["org_slug"] = self.kwargs["slug"]
        kwargs["user"] = get_user_model()
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["org"] = Organisation.objects.get(slug=self.kwargs["slug"])
        return context

    def get_success_url(self):
        return reverse_lazy("organisations:detail", args=[self.kwargs["slug"]])


class EngagementEventCreateFromCaf(FormView):
    fields = "__all__"
    form_class = EngagementEventCreateForm
    template_name = "snippets/event_form_base.html"

    def form_valid(self, form):
        ee = form.save(commit=False)
        ee.user = self.request.user
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["org_slug"] = self.kwargs.get("slug")
        kwargs["user"] = get_user_model()
        kwargs["caf"] = self.kwargs.get("caf_id")
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        return context

    def get_success_url(self):
        org_slug = CAF.objects.get(pk=self.kwargs["caf_id"]).organisation.slug
        return reverse_lazy("organisations:detail", args=[org_slug])


class SingleDateTimeEventCreate(FormView):
    template_name = "single_datetime_event_create.html"
    form_class = CreateSimpleDateTimeEventForm
    success_url = reverse_lazy("organisations:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        if self.kwargs.get("org_slug"):
            context["org"] = Organisation.objects.get(slug=self.kwargs["org_slug"])
            return context
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        kwargs["org_slug"] = self.kwargs.get("org_slug")
        kwargs["event_type"] = self.kwargs.get("event_type")
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

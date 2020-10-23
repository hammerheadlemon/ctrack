import datetime
import itertools

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView

from ctrack.organisations.models import Organisation
from ctrack.register.models import SingleDateTimeEvent, CAFSingleDateEvent, CAFTwinDateEvent

User = get_user_model()


class UserDetailView(DetailView):
    model = User

    # This names the field in the model that contains the slug. Want it to be thise so that is a good
    # citizen to be used in a URL
    slug_field = "username"

    # the name of the URLConf keyword argument that contains the slug. By default, slug_url_kwarg is 'slug'.
    # we have to pass 'username' as the argument when testing UserDetailView because of this.
    slug_url_kwarg = "username"

    def _comp_dates(self, event):
        if isinstance(event.date, datetime.datetime):
            return event.date.date()
        else:
            return event.date

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        user = self.request.user
        lead_oes = Organisation.objects.filter(lead_inspector=user).order_by("name")
        _single_date_events = SingleDateTimeEvent.objects.filter(user=user).order_by("date")
        _caf_single_date_events = CAFSingleDateEvent.objects.order_by("date")
        _caf_twin_date_events = CAFTwinDateEvent.objects.order_by("date")
        _combined = list(itertools.chain(_caf_twin_date_events, _caf_single_date_events, _single_date_events))
        all_events = sorted(_combined, key=self._comp_dates, reverse=True)
        for event in all_events:
            try:
                org = event.participants.first().organisation
                setattr(event, "organisation", org)
            except AttributeError:
                setattr(event, "organisation", None)
        all_events = sorted(_combined, key=self._comp_dates, reverse=True)
        context["all_events"] = all_events
        context["lead_oes"] = lead_oes
        return context


user_detail_view = UserDetailView.as_view()


class UserUpdateView(UpdateView):
    model = User
    fields = ["name", "first_name", "last_name"]

    def get_success_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})

    def get_object(self):
        return User.objects.get(username=self.request.user.username)

    def form_valid(self, form):
        messages.add_message(
            self.request, messages.INFO, _("Infos successfully updated")
        )
        return super().form_valid(form)


user_update_view = UserUpdateView.as_view()


class UserRedirectView(RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse("core:home")


#    def get_redirect_url(self):
#        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()

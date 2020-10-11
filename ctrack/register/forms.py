from crispy_forms.helper import FormHelper
from crispy_forms.layout import Button, ButtonHolder, Layout, Submit, Hidden, Field
from django import forms
from django.shortcuts import get_object_or_404
from django.urls import reverse

from ctrack.caf.models import CAF
from ctrack.organisations.models import Person, Organisation
from ctrack.register.models import (
    EngagementEvent,
    EngagementType,
    MeetingEvent,
    CAFSingleDateEvent,
)


class AddMeetingForm(forms.ModelForm):
    class Meta:
        model = MeetingEvent
        fields = [
            "type_descriptor",
            "short_description",
            "datetime",
            "comments",
            "location",
        ]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

    def save(self):
        form = super().save(commit=False)
        form.user = self.user
        form.save()
        return form


class CAFSingleDateEventForm(forms.ModelForm):
    class Meta:
        model = CAFSingleDateEvent
        fields = [
            "type_descriptor",
            "related_caf",
            "short_description",
            "date",
            "comments",
        ]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

    def save(self):
        form = super().save(commit=False)
        form.user = self.user
        form.save()
        return form


class EngagementEventCreateForm(forms.ModelForm):
    def __init__(self, user, caf=None, org_slug=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if caf:
            org = CAF.objects.get(pk=caf).organisation
            cancel_redirect = reverse("caf:detail", args=[caf])
            self.fields["related_caf"].initial = caf
            self.fields["participants"].queryset = Person.objects.filter(
                organisation__pk=org.pk
            )
            self.fields["type"].queryset = EngagementType.objects.all().order_by(
                "descriptor"
            )
            self.helper = FormHelper(self)
            self.helper.layout = Layout(
                Field("type"),
                "short_description",
                "participants",
                "related_caf",
                # "user",
                Hidden("user", "none"),
                "date",
                "end_date",
                "response_date_requested",
                "response_received",
                "document_link",
                "comments",
                ButtonHolder(
                    Submit("submit", "Submit", css_class="btn-primary"),
                    Button(
                        "cancel",
                        "Cancel",
                        onclick=f"location.href='{cancel_redirect}';",
                        css_class="btn-danger",
                    ),
                ),
            )
        else:
            org = get_object_or_404(Organisation, slug=org_slug)
            cancel_redirect = reverse("organisations:detail", args=[org_slug])
            selectable_people = Person.objects.filter(organisation__slug=org_slug)
            self.fields["participants"].queryset = selectable_people
            self.fields["participants"].initial = selectable_people.first()
            self.fields["type"].queryset = EngagementType.objects.all().order_by(
                "descriptor"
            )
            self.fields["related_caf"].queryset = org.caf_set.all()
            self.fields["related_caf"].label = "Related CAFs"
            self.helper = FormHelper(self)
            self.helper.layout = Layout(
                Field("type"),
                "short_description",
                "participants",
                "related_caf",
                # "user",
                Hidden("user", "none"),
                "date",
                "end_date",
                "response_date_requested",
                "response_received",
                "document_link",
                "comments",
                ButtonHolder(
                    Submit("submit", "Submit", css_class="btn-primary"),
                    Button(
                        "cancel",
                        "Cancel",
                        onclick=f"location.href='{cancel_redirect}';",
                        css_class="btn-danger",
                    ),
                ),
            )

    def save(self, commit=True):
        ee = super().save(commit=False)
        if commit:
            ee.save()
            self.save_m2m()  # so that we also save the peoples!
        return ee

    class Meta:
        model = EngagementEvent
        fields = "__all__"
        exclude = ["user"]
        widgets = {
            "date": forms.DateTimeInput(attrs={"type": "date"}),
            "response_date_requested": forms.DateTimeInput(attrs={"type": "date"}),
            "response_received": forms.DateTimeInput(attrs={"type": "date"}),
            "end_date": forms.DateTimeInput(attrs={"type": "date"}),
        }

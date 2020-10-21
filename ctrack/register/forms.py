from crispy_forms.helper import FormHelper
from crispy_forms.layout import Button, ButtonHolder, Field, Hidden, Layout, Submit
from django import forms
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.safestring import mark_safe

from ctrack.caf.models import CAF
from ctrack.organisations.models import Organisation, Person
from ctrack.register.models import (
    CAFSingleDateEvent,
    CAFTwinDateEvent,
    EngagementEvent,
    EngagementType,
    SingleDateTimeEvent,
    NoteEvent,
)


class CreateNoteEventForm(forms.ModelForm):
    class Meta:
        model = NoteEvent
        fields = [
            "short_description",
            "organisation",
            "comments",
            "private",
            "url",
            "requested_response_date",
            "response_received_date",
        ]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)
        self.fields["organisation"].queryset = Organisation.objects.all().order_by('name')

    def save(self, commit=True, **kwargs):
        new_note = super().save(commit=False)
        new_note.user = self.user
        new_note.save()
        self.save_m2m()
        return new_note


class CreateSimpleDateTimeEventForm(forms.ModelForm):
    class Meta:
        model = SingleDateTimeEvent
        fields = [
            "type_descriptor",
            "private",
            "short_description",
            "datetime",
            "participants",
            "requested_response_date",
            "response_received_date",
            "url",
            "location",
            "comments",
        ]
        widgets = {"participants": forms.CheckboxSelectMultiple()}

    def __init__(self, *args, **kwargs):
        self.event_type = None
        self.user = kwargs.pop("user")
        self.org_slug = kwargs.pop("org_slug")
        try:
            self.event_type = kwargs.pop("event_type")
        except KeyError:
            pass
        super().__init__(*args, **kwargs)
        if self.org_slug:
            org = Organisation.objects.get(slug=self.org_slug)
            self.fields["participants"].queryset = org.get_people()
            self.fields["participants"].help_text = mark_safe(
                f"Click to select participants from {org}. <strong>IMPORTANT:</strong>"
                f"You must select at least one participant."
            )
            if self.event_type:
                self.fields["type_descriptor"].initial = self.event_type
        else:
            self.fields["participants"].widget = forms.HiddenInput()

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get("datetime")
        if not date:
            return cleaned_data
        # WOOO - walrus operator
        if requested := cleaned_data.get("requested_response_date"):
            if requested < date.date():
                raise ValidationError("Requested response cannot be before date.")
        return cleaned_data

    def save(self, commit=True, **kwargs):
        new_event = super().save(commit=False)
        new_event.user = self.user
        new_event.save()
        self.save_m2m()
        return new_event


class CAFSingleDateEventForm(forms.ModelForm):
    class Meta:
        model = CAFSingleDateEvent
        fields = [
            "type_descriptor",
            "date",
            "short_description",
            "document_link",
            "comments",
        ]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        self.caf_id = kwargs.pop("caf_id")
        super().__init__(*args, **kwargs)

    def save(self, **kwargs):
        form = super().save(commit=False)
        form.user = self.user
        form.related_caf = CAF.objects.get(id=self.caf_id)
        form.save()
        return form


class CAFTwinDateEventForm(forms.ModelForm):
    # This constraint in the form prevents two such objects being created
    # for the same CAF with the same start date, which does not make sense.
    def clean_start_date(self):
        data = self.cleaned_data["start_date"]
        caf = self.cleaned_data["related_caf"]
        existing_obj = (
            CAFTwinDateEvent.objects.filter(start_date=data)
            .filter(related_caf=caf)
            .first()
        )
        if existing_obj:
            raise ValidationError(
                "You cannot have two CAF events starting on the same date."
            )
        return data

    class Meta:
        model = CAFTwinDateEvent
        fields = [
            "type_descriptor",
            "related_caf",
            "short_description",
            "start_date",
            "end_date",
            "comments",
        ]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

    def save(self, **kwargs):
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

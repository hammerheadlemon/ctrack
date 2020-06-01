from crispy_forms.helper import FormHelper
from crispy_forms.layout import Button, ButtonHolder, Layout, Submit
from django import forms
from django.urls import reverse

from ctrack.register.models import EngagementEvent


class EngagementEventCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        cancel_redirect = reverse("core:home")
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            "type",
            "short_description",
            "participants",
            "user",
            "date",
            "end_date",
            "document_link",
            "response_date_requested",
            "response_received",
            "related_caf",
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
        widgets = {
            "date": forms.DateTimeInput(attrs={"type": "date"}),
            "end_date": forms.DateTimeInput(attrs={"type": "date"}),
        }

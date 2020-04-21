from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Button, Hidden
from django import forms
from django.urls import reverse

from ctrack.organisations.models import Organisation


class OrganisationCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        cancel_redirect = reverse("organisations:list")
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                f"Create a new Organisation",
                "name",
                "submode",
                "oes",
                "designation_type",
                "registered_company_name",
                "registered_company_number",
                "updated_by",
                "comments",
                "active"
            ),
            ButtonHolder(
                Submit("submit", "Submit", css_class="btn-primary"),
                Button("cancel", "Cancel", onclick=f"location.href='{cancel_redirect}';", css_class="btn-danger")
            )
        )

    class Meta:
        model = Organisation
        fields = ["name", "submode", "oes", "designation_type",
                  "registered_company_name", "registered_company_number",
                  "updated_by", "comments", "active"]

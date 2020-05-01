from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Button, Field
from django import forms
from django.urls import reverse

from ctrack.organisations.models import Organisation, Address


class OrganisationCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        cancel_redirect = reverse("organisations:list")
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                "",
                Field("name", css_class="form-control-lg"),
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
        labels = {
            "oes": "OES"
        }
        help_texts = {
            "submode": "e.g. Rail Maintenance, TOC, etc...",
            "updated_by": "Name of staff member/inspector creating this record",
            "active": "Is this company an active participant in the NIS compliance regime?",
            "designation_type": "This is probably defined in the Reguation",
        }


class AddressCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                "type",
                "line1",
                "line2",
                "line3",
                "city",
                "county",
                "postcode",
                "country",
                "other_details"
            )
        )

    class Meta:
        model = Address
        fields = ('type', 'line1', 'line2', 'line3', 'city', 'county', 'postcode',
                  'country', 'other_details')

    # def __init__(self, *args, **kwargs):
    #     self.org = kwargs.pop("org")
    #     super().__init__(*args, **kwargs)
    #
    # def save(self):
    #     address = super().save(commit=False)
    #     address.organisation = self.org
    #     address.organisation.save()
    #     return address

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Button, Field
from django import forms
from django.urls import reverse

from ctrack.organisations.models import Organisation, Address


class OrganisationCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs["class"] = "form-control"
        self.fields["submode"].widget.attrs["class"] = "form-control"
        self.fields["oes"].widget.attrs["class"] = "form-check-input"
        self.fields["designation_type"].widget.attrs["class"] = "form-control"
        self.fields["registered_company_name"].widget.attrs["class"] = "form-control"

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
            "registered_company_name": "Probably different from the Organisation name"
        }


class AddressCreateForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ('type', 'line1', 'line2', 'line3', 'city', 'county', 'postcode',
                  'country', 'other_details')

    def __init__(self, *args, **kwargs):
        # self.org = kwargs.pop("org")
        super().__init__(*args, **kwargs)

    def save(self):
        address = super().save(commit=False)
        address.organisation = self.org
        address.organisation.save()
        return address

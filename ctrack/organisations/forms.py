from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django import forms
from django.forms import inlineformset_factory

from ctrack.organisations.models import Organisation, Address


class OrganisationCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs["class"] = "form-control form-control-lg"
        self.fields["submode"].widget.attrs["class"] = "form-control"
        self.fields["oes"].widget.attrs["class"] = "form-check-input"
        self.fields["oes"].widget.attrs["type"] = "checkbox"
        self.fields["designation_type"].widget.attrs["class"] = "form-control"
        self.fields["registered_company_name"].widget.attrs["class"] = "form-control"
        self.fields["registered_company_number"].widget.attrs["class"] = "form-control"
        self.fields["comments"].widget.attrs["class"] = "form-control"

    class Meta:
        model = Organisation
        fields = ["name", "submode", "oes", "designation_type",
                  "registered_company_name", "registered_company_number",
                  "comments", "active"]
        labels = {
            "oes": "OES"
        }
        help_texts = {
            "name": "Name of the organisation",
            "submode": "e.g. Rail Maintenance, TOC, etc...",
            "active": "Is this company an active participant in the NIS compliance regime?",
            "designation_type": "This is probably defined in the Regulation",
        }


class AddressCreateForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ('type', 'line1', 'line2', 'line3', 'city', 'county', 'postcode',
                  'country', 'other_details')


# https://dev.to/zxenia/django-inline-formsets-with-class-based-views-and-crispy-forms-14o6
# good advice on setting up the inlineformset - with crispy forms too
AddressInlineFormSet = inlineformset_factory(Organisation, Address,
                                             fields=("type", "line1", "line2", "line3", "city",
                                                     "county", "postcode", "country", "other_details"),
                                             form=AddressCreateForm)


class OrganisationInlineFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_method = "post"
        self.layout = Layout(
            "line1",
            "line2"
        )
        self.render_required_fields = True
        self.add_input(Submit("submit", "Save"))

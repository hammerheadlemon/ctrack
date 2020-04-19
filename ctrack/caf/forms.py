from crispy_forms.helper import FormHelper
from crispy_forms.layout import Button, Field, Hidden
from crispy_forms.layout import ButtonHolder
from crispy_forms.layout import Fieldset
from crispy_forms.layout import Layout
from crispy_forms.layout import Submit
from django import forms
from django.forms import inlineformset_factory

from ctrack.caf.models import ApplicableSystem
from ctrack.caf.models import CAF

CAFCreateInlineFormset = inlineformset_factory(
    CAF, ApplicableSystem, fields=("name", "organisation"), extra=2)


class ApplicableSystemCreateFromOrgForm(forms.ModelForm):

    def __init__(self, org_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                "Create a new System",
                Field("name", css_class="form-control form-control-sm"),
                Field("description", css_class="form-control form-control-sm"),
                Hidden("organisation", org_id),
                Field("caf", css_class="form-control form-control-sm")
            ),
            ButtonHolder(
                Submit("submit", "Submit", css_class="btn-primary"),
                Button("cancel", "Cancel", css_class="btn-danger")
            )
        )

    class Meta:
        model = ApplicableSystem
        fields = ["name", "description", "caf", "organisation"]


class ApplicableSystemCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                "Create a new System",
                Field("name", css_class="form-control form-control-sm"),
                Field("description", css_class="form-control form-control-sm"),
                Field("organisation", css_class="form-control form-control-sm"),
                Field("caf", css_class="form-control form-control-sm")
            ),
            ButtonHolder(
                Submit("submit", "Submit", css_class="btn-primary"),
                Button("cancel", "Cancel", css_class="btn-danger")
            )
        )

    class Meta:
        model = ApplicableSystem
        fields = ["name", "description", "organisation", "caf"]

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Button
from crispy_forms.layout import ButtonHolder
from crispy_forms.layout import Fieldset
from crispy_forms.layout import Layout
from crispy_forms.layout import Submit

from django import forms

from django.urls import reverse

from django.forms import inlineformset_factory

from ctrack.caf.models import CAF
from ctrack.caf.models import ApplicableSystem, DocumentFile
from ctrack.organisations.models import Organisation
from django.forms.models import ModelMultipleChoiceField

CAFCreateInlineFormset = inlineformset_factory(
    CAF, ApplicableSystem, fields=("name", "organisation"), extra=2)


class ApplicableSystemCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                "Create a new System",
                "name",
                "description",
                "organisation",
                "caf",
            ),
            ButtonHolder(
                Submit("submit", "Submit", css_class="btn-primary")
            )
        )

    class Meta:
        model = ApplicableSystem
        fields = ["name", "description", "organisation", "caf"]

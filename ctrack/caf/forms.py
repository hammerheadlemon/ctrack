from crispy_forms.helper import FormHelper
from crispy_forms.layout import Button
from crispy_forms.layout import ButtonHolder
from crispy_forms.layout import Fieldset
from crispy_forms.layout import Layout
from crispy_forms.layout import Submit
from django import forms

from ctrack.caf.models import CAF


class CAFForm(forms.ModelForm):
    class Meta:
        model = CAF
        fields = ["owner", "essential_system"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_class = "form-group"
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Fieldset("Create/Edit CAF", "owner", "essential_system"),
            ButtonHolder(Submit("submit", "Submit"), Button("cancel", "Cancel")),
        )

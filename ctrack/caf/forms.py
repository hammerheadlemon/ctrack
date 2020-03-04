from crispy_forms.helper import FormHelper
from crispy_forms.layout import Button
from crispy_forms.layout import ButtonHolder
from crispy_forms.layout import Fieldset
from crispy_forms.layout import Layout
from crispy_forms.layout import Submit

from django import forms

from django.urls import reverse

from django.forms import ModelChoiceField

from ctrack.caf.models import CAF
from ctrack.caf.models import DocumentFile


class CAFForm(forms.ModelForm):
    file = ModelChoiceField(
            queryset=DocumentFile.objects.all(),
            required=False,
            help_text="Please select an existing File. <a href='/caf/file/documentfile/create' target='_blank'>Create new File</a>" # TODO this URL does not exist
            )

    class Meta:
        model = CAF
        fields = ["file"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        cancel_redirect = reverse('caf:caf_list') # TODO this URL doesn't exist

        self.helper = FormHelper(self)
        self.helper.form_class = "form-group"
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Fieldset("Create/Edit CAF", "owner", "file"),
            ButtonHolder(Submit("submit", "Submit"), Button("cancel", "Cancel")),
        )


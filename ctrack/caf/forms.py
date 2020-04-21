from crispy_forms.helper import FormHelper
from crispy_forms.layout import Button, Field, Hidden
from crispy_forms.layout import ButtonHolder
from crispy_forms.layout import Fieldset
from crispy_forms.layout import Layout
from crispy_forms.layout import Submit
from django import forms
from django.forms import inlineformset_factory
from django.urls import reverse

from ctrack.caf.models import ApplicableSystem
from ctrack.caf.models import CAF
from ctrack.organisations.models import Organisation

CAFCreateInlineFormset = inlineformset_factory(
    CAF, ApplicableSystem, fields=("name", "organisation"), extra=2)


class ApplicableSystemCreateFromCafForm(forms.Form):
    name = forms.CharField(max_length=255)
    description = forms.CharField(widget=forms.Textarea)
    organisation = forms.ModelChoiceField(queryset=Organisation.objects.all())
    caf = forms.ModelChoiceField(queryset=CAF.objects.all())

    def __init__(self, *args, **kwargs):
        # We must pop the kwargs before we pass to super()
        # https://stackoverflow.com/a/8973101
        caf_id = kwargs.pop("caf_id")
        org_id = kwargs.pop("org_id")
        super().__init__(*args, **kwargs)
        caf = CAF.objects.get(pk=caf_id)
        cancel_redirect = reverse("caf:detail", args=[caf_id])
        self.fields['caf'].queryset = CAF.objects.filter(pk=caf_id)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                f"Create a new system for {caf}",
                Field("name", css_class="for-control form-control-sm"),
                Field("description", cass_class="form-control form-control-sm"),
                Hidden("caf", caf_id),
                Hidden("organisation", org_id),
            ),
            ButtonHolder(
                Submit("submit", "Submit", css_class="btn-primary"),
                Button("cancel", "Cancel", onclick=f"location.href='{cancel_redirect}';", css_class="btn-danger")
            )
        )


class ApplicableSystemCreateFromOrgForm(forms.Form):
    name = forms.CharField(max_length=255)
    description = forms.CharField(widget=forms.Textarea)
    organisation = forms.ModelChoiceField(queryset=Organisation.objects.all())
    caf = forms.ModelChoiceField(queryset=CAF.objects.all())

    def __init__(self, org_id, slug, org_name, org_cafs, *args, **kwargs):
        super().__init__(*args, **kwargs)
        cancel_redirect = reverse("organisations:detail", args=[slug])
        # we need to create the choices we can use for the CAF dropdown in the form
        self.fields['caf'].queryset = CAF.objects.filter(pk__in=[caf.pk for caf in org_cafs])
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                f"Create a new system for {org_name}",
                Field("name", css_class="form-control form-control-sm"),
                Field("description", css_class="form-control form-control-sm"),
                Hidden("organisation", org_id),
                Field("caf", css_class="form-control form-control-sm")
            ),
            ButtonHolder(
                Submit("submit", "Submit", css_class="btn-primary"),
                Button("cancel", "Cancel", onclick=f"location.href='{cancel_redirect}';", css_class="btn-danger")
            )
        )

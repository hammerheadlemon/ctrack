from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Button,
    ButtonHolder,
    Field,
    Fieldset,
    Hidden,
    Layout,
    Submit,
)
from django import forms
from django.forms import inlineformset_factory
from django.urls import reverse

from ctrack.caf.models import CAF, ApplicableSystem, EssentialService
from ctrack.organisations.models import Organisation

# TODO - Replace this to get inlineformet working
# CAFCreateInlineFormset = inlineformset_factory(
#     CAF, ApplicableSystem, fields=("name", "organisation"), extra=2
# )


class ApplicableSystemCreateFromCafForm(forms.Form):
    name = forms.CharField(max_length=255, help_text="System name assigned by OES")
    function = forms.CharField(widget=forms.Textarea)
    organisation = forms.ModelChoiceField(queryset=Organisation.objects.all())
    caf = forms.ModelChoiceField(queryset=CAF.objects.all())
    essential_service = forms.CharField(
        widget=forms.Textarea,
        max_length=255,
        help_text="Description of the essential service which the system suppports.",
    )
    dft_categorisation = forms.ChoiceField(
        choices=ApplicableSystem.SYSTEM_CATEGORISATION,
        help_text="Refer to documentation for description of these criteria",
    )
    oes_categorisation = forms.CharField(
        max_length=255,
        help_text="Categorisation based on OES' own internal prioritisation process.",
    )

    def __init__(self, *args, **kwargs):
        # We must pop the kwargs before we pass to super()
        # https://stackoverflow.com/a/8973101
        caf_id = kwargs.pop("caf_id")
        org_id = kwargs.pop("org_id")
        super().__init__(*args, **kwargs)
        caf = CAF.objects.get(pk=caf_id)
        cancel_redirect = reverse("caf:detail", args=[caf_id])
        self.fields["caf"].queryset = CAF.objects.filter(pk=caf_id)
        self.fields["dft_categorisation"].label = "DfT Categorisation"
        self.fields["oes_categorisation"].label = "OES Categorisation"
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                "",
                Field("name", css_class="form-control-lg"),
                "essential_service",
                "function",
                "dft_categorisation",
                "oes_categorisation",
                Hidden("caf", caf_id),
                Hidden("organisation", org_id),
            ),
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


class ApplicableSystemCreateFromOrgForm(forms.Form):
    name = forms.CharField(max_length=255)
    function = forms.CharField(widget=forms.Textarea)
    #   organisation = forms.ModelChoiceField(queryset=Organisation.objects.all())
    #   caf = forms.ModelChoiceField(queryset=CAF.objects.all())
    # essential_service = forms.CharField(
    #     widget=forms.Textarea,
    #     max_length=255,
    #     help_text="Description of the essential service which the system suppports.",
    # )
    essential_service = forms.ModelChoiceField(queryset=EssentialService.objects.all())
    dft_categorisation = forms.ChoiceField(
        choices=ApplicableSystem.SYSTEM_CATEGORISATION,
        help_text="Refer to documentation for description of these criteria",
    )
    oes_categorisation = forms.CharField(
        max_length=255,
        help_text="Categorisation based on OES' own internal prioritisation process.",
    )

    def __init__(self, org_id, slug, org_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        cancel_redirect = reverse("organisations:detail", args=[slug])
        # we need to create the choices we can use for the CAF dropdown in the form
        # self.fields["caf"].queryset = CAF.objects.filter(
        #     pk__in=[caf.pk for caf in org_cafs]
        # )
        # self.fields["caf"].label = "CAF"
        self.fields["dft_categorisation"].label = "DfT Categorisation"
        self.fields["oes_categorisation"].label = "OES Categorisation"
        self.fields["essential_service"].queryset = EssentialService.objects.filter(
            pk=org_id
        )
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                "",
                Field("name", css_class="form-control-lg"),
                "essential_service",
                "function",
                "dft_categorisation",
                "oes_categorisation",
                Hidden("organisation", org_id),
            ),
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

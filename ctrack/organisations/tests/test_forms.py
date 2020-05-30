import pytest

from ctrack.organisations.forms import AddressCreateForm
from ctrack.organisations.models import AddressType

pytestmark = pytest.mark.django_db


# https://test-driven-django-development.readthedocs.io/en/latest/05-forms.html
# is instructive

# Can the form accept an org_id? We need this.
@pytest.mark.skip("Explore how the inline form address addresses to an organisation")
def test_add_new_address_for_organisation_form(org_with_people):
    AddressCreateForm(org=org_with_people)


# Will our form raise an exception if the org_id isn't specified?
@pytest.mark.skip("Explore how the inline form address addresses to an organisation")
def test_add_new_address_init_without_org_id(org_with_people):
    with pytest.raises(KeyError):
        AddressCreateForm()


@pytest.mark.skip("Explore how the inline form address addresses to an organisation")
def test_add_new_address_with_valid_data(org_with_people):
    at = AddressType.objects.create(descriptor="Primary Address").pk
    form = AddressCreateForm(
        {
            "type": at,
            "line1": "10 Bawbags Lane",
            "line2": "Awful Area",
            "line3": "Chudleigh Meadows",
            "city": "Curstan",
            "county": "East Suncto",
            "postcode": "ET31 3PF",
            "country": "UK",
            "other_details": "There is nothing great about this place!",
        },
        org=org_with_people,
    )


@pytest.mark.skip("Explore how the inline form address addresses to an organisation")
def test_add_new_address_blank_data(org_with_people):
    form = AddressCreateForm({}, org=org_with_people)
    assert not form.is_valid()
    assert form.errors == {
        "type": ["This field is required."],
        "line1": ["This field is required."],
        "country": ["This field is required."],
        "postcode": ["This field is required."],
        "city": ["This field is required."],
    }

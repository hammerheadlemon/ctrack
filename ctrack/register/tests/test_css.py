import pytest

from ctrack.register.css import tag_attrs, Swimlane, CAFSwimlaneSlots
from ctrack.register.models import CAFSingleDateEvent, EventType

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    "e_type,css_str,id_str",
    [
        (
            EventType.CAF_INITIAL_CAF_RECEIVED.name,
            'style="background-color: green; color: white;"',
            "caf-initial-received-event",
        ),
        (
            EventType.CAF_INITIAL_REVIEW_COMPLETE.name,
            'style="background-color: green; color: white;"',
            "caf-initial-review-complete-event",
        )
    ],
)
def test_can_get_class_string(caf, user, e_type, css_str, id_str):
    event = CAFSingleDateEvent.objects.create(
        type_descriptor=e_type, related_caf=caf, date="2020-10-20", user=user
    )
    assert tag_attrs(event).inline_style == css_str
    assert tag_attrs(event).id_str == id_str


class _TestEvent(CAFSingleDateEvent):
    def __init__(self, event):
        self.type_descriptor = event


def test_swimlane_slots():
    slots = CAFSwimlaneSlots(
        initial_submitted=_TestEvent("CAF Initial Submitted"),
        # reviewed=_TestEvent("CAF Reviewed"),
        # revisions_submitted=_TestEvent("CAF Revisions Submitted"),
        # validation_agreed=_TestEvent("CAF Validation Agreed"),
        # improvement_plan_submitted=_TestEvent("Improvement Plan Submitted"),
        # improvement_plan_reviewed=_TestEvent("Improvement Plan Reviewed"),
        # improvement_plan_agreed=_TestEvent("Improvement Plan Agreed"),
    )
    assert slots.initial_submitted.type_descriptor == "CAF Initial Submitted"


def test_progress_chart_css_initial_review_only(caf, user):
    accept = (
        "<tr>\n"
        "   <td>{}</td>\n"
        '   <td style="background-color: green; color: white;">CAF_INITIAL_CAF_RECEIVED</td>\n'
        "   <td>CAF Reviewed</td>\n"
        "   <td>OES Revisions Submitted</td>\n"
        "   <td>Validation Agreed</td>\n"
        "   <td>Improvement Plan Submitted</td>\n"
        "   <td>Improvement Plan Review</td>\n"
        "</tr>\n"
    )
    org_name = caf.organisation.name
    caf_initial = CAFSingleDateEvent.objects.create(
        type_descriptor=EventType.CAF_INITIAL_CAF_RECEIVED.name,
        related_caf=caf,
        date="2020-10-20",
        user=user,
    )
    output = Swimlane(org_name, [caf_initial])
    assert output.tr == accept.format(org_name)


def test_progress_chart_css_initial_two_events(caf, user):
    accept = (
        "<tr>\n"
        "   <td>{}</td>\n"
        "   <td style=\"background-color: green; color: white;\">CAF_INITIAL_CAF_RECEIVED</td>\n"
        "   <td style=\"background-color: green; color: white;\">CAF_INITIAL_REVIEW_COMPLETE</td>\n"
        "   <td>OES Revisions Submitted</td>\n"
        "   <td>Validation Agreed</td>\n"
        "   <td>Improvement Plan Submitted</td>\n"
        "   <td>Improvement Plan Review</td>\n"
        "</tr>\n"
    )
    org_name = caf.organisation.name
    caf_initial = CAFSingleDateEvent.objects.create(
        type_descriptor=EventType.CAF_INITIAL_CAF_RECEIVED.name,
        related_caf=caf,
        date="2020-10-20",
        user=user,
    )
    caf_reviewed = CAFSingleDateEvent.objects.create(
        type_descriptor=EventType.CAF_INITIAL_REVIEW_COMPLETE.name,
        related_caf=caf,
        date="2020-10-20",
        user=user,
    )
    output = Swimlane(org_name, [caf_initial, caf_reviewed])
    assert output.tr == accept.format(org_name)

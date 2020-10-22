import pytest

from ctrack.register.css import Swimlane
from ctrack.register.models import CAFSingleDateEvent, EventType

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    "e_type,css_str,id_str",
    [
        (
            EventType.CAF_INITIAL_CAF_RECEIVED.name,
            ' style="background-color: green; color: white;"',
            "caf-initial-received-event",
        ),
        (
            EventType.CAF_INITIAL_REVIEW_COMPLETE.name,
            ' style="background-color: green; color: white;"',
            "caf-initial-review-complete-event",
        ),
    ],
)
def test_can_get_class_string(caf, user, e_type, css_str, id_str):
    org_name = caf.organisation.name
    event = CAFSingleDateEvent.objects.create(
        type_descriptor=e_type, related_caf=caf, date="2020-10-20", user=user
    )
    sl = Swimlane(org_name, [event])
    assert sl.tag_attrs(event).inline_style == css_str
    assert sl.tag_attrs(event).id_str == id_str


def test_progress_chart_css_initial_review_only(caf, user):
    accept = ("<tr>\n"
              "<td>{}</td>\n"
              "<td style=\"background-color: green; color: white;\">CAF_INITIAL_CAF_RECEIVED</td>\n"
              "<td>CAF_INITIAL_REVIEW_COMPLETE</td>\n"
              "<td>CAF_FEEDBACK_EMAILED_OES</td>\n"
              "<td>CAF_RECEIVED</td>\n"
              "<td>CAF_EMAILED_ROSA</td>\n"
              "<td>CAF_VALIDATION_SIGN_OFF</td>\n"
              "<td>CAF_VALIDATION_RECORD_EMAILED_TO_OES</td>\n"
              "<td>CAF_PEER_REVIEW_PERIOD</td>\n"
              "<td>CAF_VALIDATION_PERIOD</td>\n"
              "</tr>")
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
    accept = ("<tr>\n"
              "<td>{}</td>\n"
              "<td style=\"background-color: green; color: white;\">CAF_INITIAL_CAF_RECEIVED</td>\n"
              "<td style=\"background-color: green; color: white;\">CAF_INITIAL_REVIEW_COMPLETE</td>\n"
              "<td>CAF_FEEDBACK_EMAILED_OES</td>\n"
              "<td>CAF_RECEIVED</td>\n"
              "<td>CAF_EMAILED_ROSA</td>\n"
              "<td>CAF_VALIDATION_SIGN_OFF</td>\n"
              "<td>CAF_VALIDATION_RECORD_EMAILED_TO_OES</td>\n"
              "<td>CAF_PEER_REVIEW_PERIOD</td>\n"
              "<td>CAF_VALIDATION_PERIOD</td>\n"
              "</tr>")
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


def test_progress_chart_css_second_event(caf, user):
    accept = ("<tr>\n"
              "<td>{}</td>\n"
              "<td>CAF_INITIAL_CAF_RECEIVED</td>\n"
              "<td style=\"background-color: green; color: white;\">CAF_INITIAL_REVIEW_COMPLETE</td>\n"
              "<td>CAF_FEEDBACK_EMAILED_OES</td>\n"
              "<td>CAF_RECEIVED</td>\n"
              "<td>CAF_EMAILED_ROSA</td>\n"
              "<td>CAF_VALIDATION_SIGN_OFF</td>\n"
              "<td>CAF_VALIDATION_RECORD_EMAILED_TO_OES</td>\n"
              "<td>CAF_PEER_REVIEW_PERIOD</td>\n"
              "<td>CAF_VALIDATION_PERIOD</td>\n"
              "</tr>")
    org_name = caf.organisation.name
    caf_reviewed = CAFSingleDateEvent.objects.create(
        type_descriptor=EventType.CAF_INITIAL_REVIEW_COMPLETE.name,
        related_caf=caf,
        date="2020-10-20",
        user=user,
    )
    output = Swimlane(org_name, [caf_reviewed])
    assert output.tr == accept.format(org_name)


def test_table_row_builder(user, caf):
    e1 = CAFSingleDateEvent.objects.create(
        type_descriptor=EventType.CAF_INITIAL_CAF_RECEIVED.name,
        related_caf=caf,
        date="2020-10-20",
        user=user,
    )
    e2 = CAFSingleDateEvent.objects.create(
        type_descriptor=EventType.CAF_INITIAL_REVIEW_COMPLETE.name,
        related_caf=caf,
        date="2020-10-20",
        user=user,
    )
    org_name = caf.organisation.name
    sl = Swimlane(org_name, [e1, e2])
    assert sl.table_row_builder() == (
        "<tr>\n"
        f"<td>{caf.organisation.name}</td>\n"
        '<td style="background-color: green; color: white;">CAF_INITIAL_CAF_RECEIVED</td>\n'
        '<td style="background-color: green; color: white;">CAF_INITIAL_REVIEW_COMPLETE</td>\n'
        "<td>CAF_FEEDBACK_EMAILED_OES</td>\n"
        "<td>CAF_RECEIVED</td>\n"
        "<td>CAF_EMAILED_ROSA</td>\n"
        "<td>CAF_VALIDATION_SIGN_OFF</td>\n"
        "<td>CAF_VALIDATION_RECORD_EMAILED_TO_OES</td>\n"
        "<td>CAF_PEER_REVIEW_PERIOD</td>\n"
        "<td>CAF_VALIDATION_PERIOD</td>\n"
        "</tr>"
    )


def test_table_row_builder_with_no_events(user, caf):
    org_name = caf.organisation.name
    sl = Swimlane(org_name, [])
    assert sl.table_row_builder() == (
        "<tr>\n"
        f"<td>{caf.organisation.name}</td>\n"
        "<td>CAF_INITIAL_CAF_RECEIVED</td>\n"
        '<td>CAF_INITIAL_REVIEW_COMPLETE</td>\n'
        "<td>CAF_FEEDBACK_EMAILED_OES</td>\n"
        "<td>CAF_RECEIVED</td>\n"
        "<td>CAF_EMAILED_ROSA</td>\n"
        "<td>CAF_VALIDATION_SIGN_OFF</td>\n"
        "<td>CAF_VALIDATION_RECORD_EMAILED_TO_OES</td>\n"
        "<td>CAF_PEER_REVIEW_PERIOD</td>\n"
        "<td>CAF_VALIDATION_PERIOD</td>\n"
        "</tr>"
    )

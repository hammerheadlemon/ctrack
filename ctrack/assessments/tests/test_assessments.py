import pytest

from ctrack.assessments.models import AchievementLevel
from ctrack.assessments.models import CAFContributingOutcome
from ctrack.assessments.models import IGP

pytestmark = pytest.mark.django_db


def test_get_random_igps(full_db_fixture):
    na = AchievementLevel.objects.filter(descriptor="Not Achieved").first()
    co1 = CAFContributingOutcome.objects.get(pk=1)
    igps_co1 = IGP.objects.filter(contributing_outcome=co1,
                                  achievement_level=na)
    assert co1.designation == "A1.a"
    assert na.descriptor == "Not Achieved"
    assert igps_co1.first().descriptive_text[:5] == "IGP 1"

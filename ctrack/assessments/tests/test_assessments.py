import pytest

from ctrack.assessments.models import AchievementLevel
from ctrack.assessments.models import CAFContributingOutcome
from ctrack.assessments.models import IGP

pytestmark = pytest.mark.django_db



@pytest.mark.skip("Use once we populate the test database")
def test_get_random_igps():
    na = AchievementLevel.objects.filter(descriptor="Not Achieved").first()
    co1 = CAFContributingOutcome.objects.get(pk=1)
    igps_co1 = IGP.objects.filter(contributing_outcome=co1,
                                  achievement_level=na)
    assert False

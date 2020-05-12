import factory
from factory import Faker

from ctrack.assessments.models import AchievementLevel


class AchievementLevelFactory(factory.DjangoModelFactory):
    descriptor = Faker("text", max_nb_chars=30, ext_word_list=None)
    colour_description = Faker("text", max_nb_chars=30, ext_word_list=None)
    colour_hex = Faker("text", max_nb_chars=30, ext_word_list=None)

    class Meta:
        model = AchievementLevel


class IGPFactory(factory.DjangoModelFactory):
    achievement_level = factory.SubFactory(AchievementLevelFactory)

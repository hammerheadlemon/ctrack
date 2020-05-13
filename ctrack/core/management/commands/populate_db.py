from django.core.management import BaseCommand

from ctrack.core.utils import populate_db


class Command(BaseCommand):
    help = """
    Creates a large test fixture.
    """

    def handle(self, *args, **options):
        populate_db()

        # TODO - adapt this so that it records more than just Persons created
        self.stdout.write(
            self.style.SUCCESS(
                f"Created test fixture successfully."
            )
        )

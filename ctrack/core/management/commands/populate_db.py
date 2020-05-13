
from django.core.management import BaseCommand
from django.core.management import CommandParser
from ctrack.core.utils import populate_db


class Command(BaseCommand):
    help = """
    Creates a large test fixture.
    """

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("number", nargs=1, type=int)

    def handle(self, *args, **options):
        number = options["number"][0]
        populate_db(number)

        # TODO - adapt this so that it records more than just Persons created
        self.stdout.write(
            self.style.SUCCESS(
                f"Created {number} Person object[s]! Go forth and multiply."
            )
        )

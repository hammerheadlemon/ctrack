from django.core.management import BaseCommand


class Command(BaseCommand):
    help = """
    Creates a bunch of people and organisations for them to work in.

    python manage.py generate_people
    """


#    def add_arguments(self, parser):
#        parser.add_argument("year", nargs="+", type=int)
#
#    def handle(self, *args, **options):
#        for opt in options["year"]:
#            FinancialQuarter.objects.create(quarter=1, year=opt)
#            FinancialQuarter.objects.create(quarter=2, year=opt)
#            FinancialQuarter.objects.create(quarter=3, year=opt)
#            FinancialQuarter.objects.create(quarter=4, year=opt)
#            self.stdout.write(
#                self.style.SUCCESS(
#                    f"Created FinancialQuarter objects for the years: {opt}"
#                )
#            )

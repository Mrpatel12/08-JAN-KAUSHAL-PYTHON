from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from Services.openflights_importer import import_openflights_flights


class Command(BaseCommand):
    help = (
        "Import flight routes from the OpenFlights dataset and store them as Flight records in INR. "
        "This command can populate both national and international flights for all valid OpenFlights routes."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--max-routes",
            type=int,
            default=None,
            help="Limit the number of OpenFlights routes to import. If omitted, all valid routes are imported.",
        )
        parser.add_argument(
            "--skip-existing",
            action="store_true",
            help="Keep existing matching flights unchanged instead of updating them.",
        )
        parser.add_argument(
            "--verbose",
            action="store_true",
            help="Print progress messages during import.",
        )

    def handle(self, *args, **options):
        max_routes = options["max_routes"]
        skip_existing = options["skip_existing"]
        verbose = options["verbose"]

        self.stdout.write(self.style.NOTICE("Starting OpenFlights import..."))
        try:
            created, updated, skipped, total = import_openflights_flights(
                max_routes=max_routes,
                skip_existing=skip_existing,
                verbose=verbose,
            )
        except Exception as exc:
            raise CommandError(str(exc))

        self.stdout.write(self.style.SUCCESS(
            f"Import complete. Processed {total} routes, created {created} new flights, updated {updated}, skipped {skipped}."
        ))
        self.stdout.write(self.style.NOTICE(
            "Flights are stored in INR and marked as national/international by route country pair."
        ))

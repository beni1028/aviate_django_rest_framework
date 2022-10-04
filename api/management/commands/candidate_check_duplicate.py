from django.db import transaction
from django.core.management.base import BaseCommand
from django.db.models import Count, Max


from api.models import Candidate

class Command(BaseCommand):
    help = "Migrating Data from Candidate Table to User Table"

    @transaction.atomic
    def handle(self, *args, **kwargs):

        self.stdout.write("Finding and deleteing duplicates")

        unique_fields = ['email',]

        duplicates = (
            Candidate.objects.values(*unique_fields)
            .order_by()
            .annotate(max_id=Max('id'), count_id=Count('id'))
            .filter(count_id__gt=1)
        )

        self.stdout.write(f"Total duplicates found: {duplicates.count()}")
        self.stdout.write("All Duplicates")
        for duplicate in duplicates:
            self.stdout.write(f'{duplicate}')




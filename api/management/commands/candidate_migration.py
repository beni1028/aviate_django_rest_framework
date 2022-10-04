from django.db import transaction
from django.core.management.base import BaseCommand

from api.models import User, Candidate

from django.contrib.auth.models import Group


from django.db.models import Count, Max



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

        for duplicate in duplicates:
            (
                Candidate.objects
                .filter(**{x: duplicate[x] for x in unique_fields})
                .exclude(id=duplicate['max_id'])
                .delete()
            )


        self.stdout.write("Migrating data from Candidate Table to User...")

        user_group,_ = Group.objects.get_or_create(name='candidate')
        # self.stdout.write(user_group)
        candidates = Candidate.objects.all()


        for candidate in candidates:
            if not User.objects.filter(email=candidate.email).exists():
                user = User.objects.create(email=candidate.email, username=candidate.email)
                user.groups.add(user_group)
                candidate.user = user
                candidate.save()
            
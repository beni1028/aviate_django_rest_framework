from django.db import transaction
from django.core.management.base import BaseCommand

from django.contrib.auth.models import Group


class Command(BaseCommand):
    help = "Creating Groups for ACL"

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write("Creating groups for ACL...")
        user_group1 = Group.objects.bulk_create([
            Group(name='recruiter-admin'),
            Group(name='recruiter'),
            Group(name='internal'),
            Group(name='candidate'),
        ]
            )
        groups = Group.objects.all()
                # [name='recruiter-admin',name='recruiter',name='internal',name='candidate'])
        self.stdout.write(f'Total groups created:{groups.count()}')

        for group in groups:
            self.stdout.write(f'{group}')


        

            
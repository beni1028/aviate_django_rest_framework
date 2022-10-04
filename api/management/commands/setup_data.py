import random

from django.db import transaction
from django.core.management.base import BaseCommand

from api.models import Candidate


from api.factories import CandidateFactory


NUM_Candidates = 5000


class Command(BaseCommand):
    help = "Generates test data"

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write("Deleting old data...")
        models = [Candidate]
        for m in models:
            m.objects.all().delete()

        self.stdout.write("Creating/adding new data...")
        # Create all the users
        candidate = []
        for _ in range(NUM_Candidates):
            candidate_fake = CandidateFactory()
            candidate.append(candidate_fake)

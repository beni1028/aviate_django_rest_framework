#  factories.py
import factory
from factory.django import DjangoModelFactory

from api.models import Candidate

# Defining a factory
class CandidateFactory(DjangoModelFactory):
    class Meta:
        model = Candidate

    email = factory.Faker("email")
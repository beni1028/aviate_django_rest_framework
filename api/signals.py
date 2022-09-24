from django.db.models.signals import post_save
from .models import Applicant
from django.dispatch import receiver
 

@receiver(post_save, sender=Applicant) 
def update_uid(sender, instance, created, **kwargs):
    if created:
        instance.gen_uid_and_slug()

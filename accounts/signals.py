from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile

@receiver(post_save, sender=Profile)
def profile_creation_confirmation(sender, instance, created, **kwargs):
    print("profile been created successfully")

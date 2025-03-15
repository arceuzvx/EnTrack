from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import UserProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create a UserProfile for every new User"""
    if created:
        UserProfile.objects.create(user=instance, username=instance.username)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save the UserProfile when the User is saved"""
    instance.profile.save() 
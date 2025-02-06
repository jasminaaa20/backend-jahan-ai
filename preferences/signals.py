from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.db import transaction
from .models import AccountSettings, NotificationSettings, ThemeSettings, PrivacySettings

User = get_user_model()

@receiver(post_save, sender=User)
def create_user_preferences(sender, instance, created, **kwargs):
    """
    Signal handler to create all preference instances for a new user.
    This keeps preference creation logic within the preferences app.
    """
    if created:
        with transaction.atomic():
            AccountSettings.objects.create(user=instance)
            NotificationSettings.objects.create(user=instance)
            ThemeSettings.objects.create(user=instance)
            PrivacySettings.objects.create(user=instance)

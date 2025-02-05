from django.db import models
from django.contrib.auth.models import User

class AccountSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="account_settings")
    preferred_language = models.CharField(max_length=10, default='en')
    time_zone = models.CharField(max_length=50, default='UTC')
    
    def __str__(self):
        return f"{self.user.username} Account Settings"

class NotificationSettings(models.Model):
    NOTIFICATION_FREQUENCY_CHOICES = [
        ('instant', 'Instant'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="notification_settings")
    email_notifications = models.BooleanField(default=True)
    push_notifications = models.BooleanField(default=False)
    notification_frequency = models.CharField(max_length=10, choices=NOTIFICATION_FREQUENCY_CHOICES, default='instant')

    def __str__(self):
        return f"{self.user.username} Notification Settings"

class ThemeSettings(models.Model):
    THEME_CHOICES = [
        ('light', 'Light'),
        ('dark', 'Dark'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="theme_settings")
    theme = models.CharField(max_length=10, choices=THEME_CHOICES, default='light')
    font_size = models.IntegerField(default=14)

    def __str__(self):
        return f"{self.user.username} Theme Settings"

class PrivacySettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="privacy_settings")
    profile_visibility = models.BooleanField(default=True)
    data_sharing = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} Privacy Settings"

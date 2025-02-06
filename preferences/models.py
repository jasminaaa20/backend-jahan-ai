from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

class BasePreferenceModel(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="%(class)s"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class AccountSettings(BasePreferenceModel):
    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('es', 'Spanish'),
        ('fr', 'French'),
        # Add more languages as needed
    ]
    
    DATE_FORMAT_CHOICES = [
        ('YYYY-MM-DD', 'ISO Format'),
        ('DD/MM/YYYY', 'European Format'),
        ('MM/DD/YYYY', 'US Format'),
    ]

    language = models.CharField(
        max_length=10, 
        choices=LANGUAGE_CHOICES, 
        default='en'
    )
    timezone = models.CharField(max_length=50, default='UTC')
    date_format = models.CharField(
        max_length=20, 
        choices=DATE_FORMAT_CHOICES, 
        default='YYYY-MM-DD'
    )

    class Meta:
        verbose_name_plural = 'Account Settings'

class NotificationSettings(BasePreferenceModel):
    FREQUENCY_CHOICES = [
        ('never', 'Never'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ]

    email_notifications = models.BooleanField(default=True)
    push_notifications = models.BooleanField(default=True)
    notification_frequency = models.CharField(
        max_length=10,
        choices=FREQUENCY_CHOICES,
        default='daily'
    )
    marketing_emails = models.BooleanField(default=False)
    system_notifications = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Notification Settings'

class ThemeSettings(BasePreferenceModel):
    THEME_CHOICES = [
        ('light', 'Light'),
        ('dark', 'Dark'),
        ('system', 'System Default'),
    ]
    
    LAYOUT_CHOICES = [
        ('compact', 'Compact'),
        ('comfortable', 'Comfortable'),
        ('grid', 'Grid'),
    ]

    theme = models.CharField(
        max_length=10,
        choices=THEME_CHOICES,
        default='system'
    )
    font_size = models.IntegerField(
        default=14,
        validators=[MinValueValidator(8), MaxValueValidator(32)]
    )
    layout = models.CharField(
        max_length=15,
        choices=LAYOUT_CHOICES,
        default='comfortable'
    )
    high_contrast = models.BooleanField(default=False)
    reduced_motion = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Theme Settings'

class PrivacySettings(BasePreferenceModel):
    VISIBILITY_CHOICES = [
        ('public', 'Public'),
        ('private', 'Private'),
        ('friends', 'Friends Only'),
    ]

    profile_visibility = models.CharField(
        max_length=10,
        choices=VISIBILITY_CHOICES,
        default='private'
    )
    data_sharing = models.BooleanField(default=False)
    show_online_status = models.BooleanField(default=True)
    allow_search = models.BooleanField(default=True)
    two_factor_enabled = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Privacy Settings'
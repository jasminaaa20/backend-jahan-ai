from rest_framework import serializers
from .models import AccountSettings, NotificationSettings, ThemeSettings, PrivacySettings

class AccountSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountSettings
        fields = ['preferred_language', 'time_zone']

class NotificationSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationSettings
        fields = ['email_notifications', 'push_notifications', 'notification_frequency']

class ThemeSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThemeSettings
        fields = ['theme', 'font_size']

class PrivacySettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivacySettings
        fields = ['profile_visibility', 'data_sharing']

class AllPreferencesSerializer(serializers.Serializer):
    account = AccountSettingsSerializer()
    notifications = NotificationSettingsSerializer()
    theme = ThemeSettingsSerializer()
    privacy = PrivacySettingsSerializer()

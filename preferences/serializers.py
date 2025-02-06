from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    AccountSettings,
    NotificationSettings,
    ThemeSettings,
    PrivacySettings
)

User = get_user_model()

class AccountSettingsSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = AccountSettings
        fields = ['username', 'email', 'language', 'timezone', 'date_format']

    def validate_timezone(self, value):
        # Add timezone validation if needed
        return value

class NotificationSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationSettings
        exclude = ['user', 'created_at', 'updated_at']

    def validate(self, data):
        if not data.get('email_notifications') and data.get('marketing_emails'):
            raise serializers.ValidationError({
                "marketing_emails": "Cannot enable marketing emails while email notifications are disabled"
            })
        return data

class ThemeSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThemeSettings
        exclude = ['user', 'created_at', 'updated_at']

    def validate_font_size(self, value):
        if value % 2 != 0:
            raise serializers.ValidationError("Font size must be an even number")
        return value

class PrivacySettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivacySettings
        exclude = ['user', 'created_at', 'updated_at']

    def validate(self, data):
        if data.get('profile_visibility') == 'public' and not data.get('allow_search'):
            raise serializers.ValidationError({
                "allow_search": "Search must be enabled for public profiles"
            })
        return data
from rest_framework import serializers
from .models import AccountSettings, NotificationSettings, ThemeSettings, PrivacySettings
from django.contrib.auth.models import User

class AccountSettingsSerializer(serializers.ModelSerializer):
    # Expose user fields via nested sources.
    username = serializers.CharField(source='user.username', required=False)
    email = serializers.EmailField(source='user.email', required=False)
    password = serializers.CharField(
        write_only=True,
        required=False,
        style={'input_type': 'password'}
    )

    class Meta:
        model = AccountSettings
        fields = ['username', 'email', 'password', 'preferred_language', 'time_zone']

    def update(self, instance, validated_data):
        # Extract user-related data (pop nested "user" data)
        user_data = validated_data.pop('user', {})
        password = validated_data.pop('password', None)
        user = instance.user
        if 'username' in user_data:
            user.username = user_data['username']
        if 'email' in user_data:
            user.email = user_data['email']
        if password:
            user.set_password(password)
        user.save()
        # Update the AccountSettings fields
        return super().update(instance, validated_data)

class NotificationSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationSettings
        fields = ['email_notifications', 'push_notifications', 'notification_frequency']

class ThemeSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThemeSettings
        fields = ['theme', 'font_size', 'layout']

class PrivacySettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivacySettings
        fields = ['profile_visibility', 'data_sharing']

class AllPreferencesSerializer(serializers.Serializer):
    account = AccountSettingsSerializer()
    notifications = NotificationSettingsSerializer()
    theme = ThemeSettingsSerializer()
    privacy = PrivacySettingsSerializer()

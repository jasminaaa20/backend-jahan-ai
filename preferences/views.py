# preferences/views.py

from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import AccountSettings, NotificationSettings, ThemeSettings, PrivacySettings
from .serializers import (
    AccountSettingsSerializer,
    NotificationSettingsSerializer,
    ThemeSettingsSerializer,
    PrivacySettingsSerializer,
    AllPreferencesSerializer
)

# Combined view to retrieve all preferences
class AllPreferencesView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        account = AccountSettings.objects.get(user=request.user)
        notifications = NotificationSettings.objects.get(user=request.user)
        theme = ThemeSettings.objects.get(user=request.user)
        privacy = PrivacySettings.objects.get(user=request.user)

        data = {
            'account': AccountSettingsSerializer(account).data,
            'notifications': NotificationSettingsSerializer(notifications).data,
            'theme': ThemeSettingsSerializer(theme).data,
            'privacy': PrivacySettingsSerializer(privacy).data,
        }
        return Response(data)

# Individual views for each preference type
class AccountSettingsView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AccountSettingsSerializer

    def get_object(self):
        return AccountSettings.objects.get(user=self.request.user)

class NotificationSettingsView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = NotificationSettingsSerializer

    def get_object(self):
        return NotificationSettings.objects.get(user=self.request.user)

class ThemeSettingsView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ThemeSettingsSerializer

    def get_object(self):
        return ThemeSettings.objects.get(user=self.request.user)

class PrivacySettingsView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PrivacySettingsSerializer

    def get_object(self):
        return PrivacySettings.objects.get(user=self.request.user)

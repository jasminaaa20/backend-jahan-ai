from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import (
    AccountSettings,
    NotificationSettings,
    ThemeSettings,
    PrivacySettings
)
from .serializers import (
    AccountSettingsSerializer,
    NotificationSettingsSerializer,
    ThemeSettingsSerializer,
    PrivacySettingsSerializer
)

class BasePreferenceView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(self.model, user=self.request.user)

class AccountSettingsView(BasePreferenceView):
    serializer_class = AccountSettingsSerializer
    model = AccountSettings

class NotificationSettingsView(BasePreferenceView):
    serializer_class = NotificationSettingsSerializer
    model = NotificationSettings

class ThemeSettingsView(BasePreferenceView):
    serializer_class = ThemeSettingsSerializer
    model = ThemeSettings

class PrivacySettingsView(BasePreferenceView):
    serializer_class = PrivacySettingsSerializer
    model = PrivacySettings

class AllPreferencesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        account = get_object_or_404(AccountSettings, user=request.user)
        notifications = get_object_or_404(NotificationSettings, user=request.user)
        theme = get_object_or_404(ThemeSettings, user=request.user)
        privacy = get_object_or_404(PrivacySettings, user=request.user)

        return Response({
            'account': AccountSettingsSerializer(account).data,
            'notifications': NotificationSettingsSerializer(notifications).data,
            'theme': ThemeSettingsSerializer(theme).data,
            'privacy': PrivacySettingsSerializer(privacy).data
        })
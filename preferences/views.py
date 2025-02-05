from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

from .models import AccountSettings, NotificationSettings, ThemeSettings, PrivacySettings
from .serializers import (
    AccountSettingsSerializer,
    NotificationSettingsSerializer,
    ThemeSettingsSerializer,
    PrivacySettingsSerializer,
    AllPreferencesSerializer
)

class UserPreferenceMixin:
    """
    Mixin to retrieve the user's preference object using the reverse relationship.
    Expects the subclass to define a `preference_name` attribute corresponding
    to the related_name on the User model.
    """
    def get_object(self):
        try:
            # Use the reverse relationship (e.g. request.user.account_settings)
            return getattr(self.request.user, self.preference_name)
        except ObjectDoesNotExist:
            raise Http404(f"{self.preference_name} not found for user.")

class AllPreferencesView(APIView):
    """
    Combined view that retrieves all of the user's preferences.
    Uses the AllPreferencesSerializer to return a combined representation.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            # Access each preference via the reverse relationship
            account = request.user.account_settings
            notifications = request.user.notification_settings
            theme = request.user.theme_settings
            privacy = request.user.privacy_settings
        except ObjectDoesNotExist:
            raise Http404("One or more preference objects not found.")

        # Pass the model instances in a dictionary to the combined serializer
        data = {
            'account': account,
            'notifications': notifications,
            'theme': theme,
            'privacy': privacy,
        }
        serializer = AllPreferencesSerializer(instance=data)
        return Response(serializer.data)

class AccountSettingsView(UserPreferenceMixin, generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AccountSettingsSerializer
    # Must match the related_name defined in AccountSettings model
    preference_name = 'account_settings'

class NotificationSettingsView(UserPreferenceMixin, generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = NotificationSettingsSerializer
    # Must match the related_name defined in NotificationSettings model
    preference_name = 'notification_settings'

class ThemeSettingsView(UserPreferenceMixin, generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ThemeSettingsSerializer
    # Must match the related_name defined in ThemeSettings model
    preference_name = 'theme_settings'

class PrivacySettingsView(UserPreferenceMixin, generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PrivacySettingsSerializer
    # Must match the related_name defined in PrivacySettings model
    preference_name = 'privacy_settings'

from django.urls import path
from .views import (
    AllPreferencesView,
    AccountSettingsView,
    NotificationSettingsView,
    ThemeSettingsView,
    PrivacySettingsView
)

urlpatterns = [
    path('', AllPreferencesView.as_view(), name='all-preferences'),
    path('account/', AccountSettingsView.as_view(), name='account-preferences'),
    path('notifications/', NotificationSettingsView.as_view(), name='notification-preferences'),
    path('theme/', ThemeSettingsView.as_view(), name='theme-preferences'),
    path('privacy/', PrivacySettingsView.as_view(), name='privacy-preferences'),
]

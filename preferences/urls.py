from django.urls import path
from .views import (
    AccountSettingsView,
    NotificationSettingsView,
    ThemeSettingsView,
    PrivacySettingsView,
    AllPreferencesView
)

urlpatterns = [
    path('all/', AllPreferencesView.as_view(), name='all-preferences'),
    path('account/', AccountSettingsView.as_view(), name='account-settings'),
    path('notifications/', NotificationSettingsView.as_view(), name='notification-settings'),
    path('theme/', ThemeSettingsView.as_view(), name='theme-settings'),
    path('privacy/', PrivacySettingsView.as_view(), name='privacy-settings'),
]
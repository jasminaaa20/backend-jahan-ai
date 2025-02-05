# authentication/tests/test_views.py

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory
from rest_framework import status
from unittest.mock import patch
from authentication.views import RegisterView
from preferences.models import NotificationSettings, ThemeSettings, PrivacySettings

class RegisterViewTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.url = reverse('register')
        self.valid_data = {
            'username': 'viewuser',
            'email': 'viewuser@example.com',
            'password': 'StrongPass123!',
            'password2': 'StrongPass123!'
        }
    
    def test_register_creates_user_and_preferences(self):
        request = self.factory.post(self.url, self.valid_data, format='json')
        response = RegisterView.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Check that the user was created
        user = User.objects.get(username='viewuser')
        self.assertIsNotNone(user)
        # Check that the default preferences objects were created for the user
        self.assertTrue(NotificationSettings.objects.filter(user=user).exists())
        self.assertTrue(ThemeSettings.objects.filter(user=user).exists())
        self.assertTrue(PrivacySettings.objects.filter(user=user).exists())
    
    def test_transaction_rollback_on_preferences_failure(self):
        # Use patch to simulate an exception when creating default preferences.
        with patch('authentication.views.create_default_preferences') as mocked_create_prefs:
            mocked_create_prefs.side_effect = Exception("Preferences creation failed")
            request = self.factory.post(self.url, self.valid_data, format='json')
            response = RegisterView.as_view()(request)
            # We expect a 400 error if preferences creation fails
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            # Verify that no user was created due to the transaction rollback.
            self.assertFalse(User.objects.filter(username='viewuser').exists())

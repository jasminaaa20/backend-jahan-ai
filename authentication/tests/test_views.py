from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from unittest.mock import patch
from preferences.models import NotificationSettings, ThemeSettings, PrivacySettings

class RegisterViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('register')
        self.valid_data = {
            'username': 'viewuser',
            'email': 'viewuser@example.com',
            'password': 'StrongPass123!',
            'password2': 'StrongPass123!'
        }
    
    def test_register_creates_user_and_preferences(self):
        response = self.client.post(self.url, self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(username='viewuser')
        self.assertTrue(NotificationSettings.objects.filter(user=user).exists())
        self.assertTrue(ThemeSettings.objects.filter(user=user).exists())
        self.assertTrue(PrivacySettings.objects.filter(user=user).exists())
    
    def test_transaction_rollback_on_preferences_failure(self):
        with patch('preferences.signals.create_user_preferences') as mocked_create_prefs:
            mocked_create_prefs.side_effect = Exception("Preferences creation failed") 
            response = self.client.post(self.url, self.valid_data, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertFalse(User.objects.filter(username='viewuser').exists())

class ChangePasswordViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('change-password')
        self.user = User.objects.create_user(username='changepassuser', email='changepass@example.com', password='OldPassword123!')
        self.client.force_authenticate(user=self.user)
    
    def test_change_password_success(self):
        data = {
            'old_password': 'OldPassword123!',
            'new_password': 'NewPassword456!',
            'new_password2': 'NewPassword456!'
        }
        response = self.client.put(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('NewPassword456!'))
    
    def test_change_password_failure(self):
        data = {
            'old_password': 'WrongOldPassword!',
            'new_password': 'NewPass567!',
            'new_password2': 'NewPass567!'
        }
        response = self.client.put(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('old_password', response.data)

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from preferences.models import NotificationSettings, ThemeSettings, PrivacySettings

class AuthenticationAPITests(APITestCase):
    def setUp(self):
        # Assuming your app urls are included without a namespace.
        # If you have namespacing, adjust the reverse() calls accordingly.
        self.register_url = reverse('register')
        self.login_url = reverse('login')
    
    def test_register_success(self):
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'StrongPassword123!',
            'password2': 'StrongPassword123!'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertIn('user', response.data)
        
        # Verify that default preferences are created for the new user
        user = User.objects.get(username='testuser')
        self.assertTrue(NotificationSettings.objects.filter(user=user).exists())
        self.assertTrue(ThemeSettings.objects.filter(user=user).exists())
        self.assertTrue(PrivacySettings.objects.filter(user=user).exists())
    
    def test_register_password_mismatch(self):
        data = {
            'username': 'testuser2',
            'email': 'test2@example.com',
            'password': 'StrongPassword123!',
            'password2': 'DifferentPassword!'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)
    
    def test_login_success(self):
        # First, create a user (using Django's built-in create_user which handles hashing)
        User.objects.create_user(username='loginuser', email='login@example.com', password='TestPassword123!')
        data = {
            'username': 'loginuser',
            'password': 'TestPassword123!'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
    
    def test_login_failure(self):
        data = {
            'username': 'nonexistent',
            'password': 'SomePassword'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data.get('detail'), 'Invalid credentials')

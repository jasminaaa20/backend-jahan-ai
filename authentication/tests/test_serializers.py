from django.test import TestCase
from django.contrib.auth.models import User
from authentication.serializers import RegisterSerializer, LoginSerializer, ChangePasswordSerializer
from rest_framework.test import APIClient, APIRequestFactory

class RegisterSerializerTests(TestCase):
    def test_valid_data_creates_user(self):
        data = {
            'username': 'serializeruser',
            'email': 'serializer@example.com',
            'password': 'ValidPassword123!',
            'password2': 'ValidPassword123!'
        }
        serializer = RegisterSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        user = serializer.save()
        self.assertEqual(user.username, data['username'])
        self.assertEqual(user.email, data['email'])
        self.assertTrue(user.check_password(data['password']))
    
    def test_password_mismatch(self):
        data = {
            'username': 'serializeruser2',
            'email': 'serializer2@example.com',
            'password': 'ValidPassword123!',
            'password2': 'MismatchPassword!'
        }
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('password', serializer.errors)

class LoginSerializerTests(TestCase):
    def test_required_fields(self):
        data = {}
        serializer = LoginSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('username', serializer.errors)
        self.assertIn('password', serializer.errors)

class ChangePasswordSerializerTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='changepassuser', email='changepass@example.com', password='OldPassword123!')
        self.factory = APIRequestFactory()
    
    def test_valid_change_password(self):
        request = self.factory.post('/', data={}, format='json')
        request.user = self.user
        
        data = {
            'old_password': 'OldPassword123!',
            'new_password': 'NewPassword456!',
            'new_password2': 'NewPassword456!'
        }
        serializer = ChangePasswordSerializer(data=data, context={'request': request})
        self.assertTrue(serializer.is_valid(), serializer.errors)
    
    def test_invalid_old_password(self):
        request = self.factory.post('/', data={}, format='json')
        request.user = self.user
        
        data = {
            'old_password': 'WrongOldPassword!',
            'new_password': 'NewPassword789!',
            'new_password2': 'NewPassword789!'
        }
        serializer = ChangePasswordSerializer(data=data, context={'request': request})
        self.assertFalse(serializer.is_valid())
        self.assertIn('old_password', serializer.errors)

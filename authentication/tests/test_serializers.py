from django.test import TestCase
from django.contrib.auth.models import User
from authentication.serializers import RegisterSerializer, LoginSerializer

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
        # The password is stored hashed so we use check_password to verify it
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

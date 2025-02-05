from django.db import transaction
from rest_framework import status, generics, serializers
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import RegisterSerializer, LoginSerializer
from preferences.models import NotificationSettings, ThemeSettings, PrivacySettings

def create_default_preferences(user):
    NotificationSettings.objects.create(
        user=user,
        notification_frequency='daily',
        email_notifications=True,
        push_notifications=True
    )
    ThemeSettings.objects.create(
        user=user,
        theme='light',
        font_size=14,
        layout='grid'
    )
    PrivacySettings.objects.create(
        user=user,
        profile_visibility=True,  # True means public
        data_sharing=False        # Adjust defaults as needed
    )

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        try:
            create_default_preferences(user)
        except Exception as e:
            # If default preferences creation fails, raise an error to roll back the transaction.
            raise serializers.ValidationError({'detail': str(e)})

        refresh = RefreshToken.for_user(user)
        return Response({
            'user': serializer.data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        # Use Django's built-in authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

from django.contrib.auth import get_user_model, authenticate, login
from django.shortcuts import render
from rest_framework import permissions, viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.views import TokenObtainPairView

from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

from .serializers import CustomTokenObtainPairSerializer
import pyrebase
import environ

User = get_user_model()

env = environ.Env()
environ.Env.read_env()

firebase = pyrebase.initialize_app({
    "apiKey": env('API_KEY'),
    "authDomain": env('AUTH_DOMAIN'),
    "projectId": env('PROJECT_ID'),
    "storageBucket": env('STORAGE_BUCKET'),
    "messagingSenderId": env('MESSAGING_SENDER_ID'),
    "appId": env('APP_ID'),
    "measurementId": env('MEASUREMENT_ID'),
    "databaseURL": ""
})
storage = firebase.storage()


@api_view(['POST'])
def check_username_exists(request):
    username = request.data.get('username')
    if not username:
        return Response({'error': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        User.objects.get(username=username)
        return Response({'username_exists': True}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'username_exists': False}, status=status.HTTP_404_NOT_FOUND)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        try:
            user = User.objects.get(email=request.data.get('email'))
            if not user.is_active:
                return Response({'detail': 'Account not activated'}, status=status.HTTP_401_UNAUTHORIZED)
            if hasattr(user, 'is_deactivated') and user.is_deactivated:
                return Response({'detail': 'Account deactivated'}, status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            return Response({'detail': 'Invalid username or password'}, status=status.HTTP_400_BAD_REQUEST)

        return super().post(request, *args, **kwargs)


def send_activation_email(user):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    activation_url = f'http://localhost:5173/auth/activate/?uid={uid}&token={token}'
    print(f'Activation URL: {activation_url}')
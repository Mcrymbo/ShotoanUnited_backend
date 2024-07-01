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

from .models import Profile, storage
from .serializers import ProfileSerializer

from .serializers import CustomTokenObtainPairSerializer

User = get_user_model()

# Helper function to upload profile
def upload_profile_picture(profile_pic):
    with profile_pic.open() as img:
        storage.child(f"profile_pics/{profile_pic.name}").put(img)
        url = storage.child(f"profile_pics/{profile_pic.name}").get_url(None)
        return url

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def perform_create(self, serializer):
        profile_instance = serializer.save()
        if 'profile_pic' in self.request.FILES:
            profile_pic_url = upload_profile_picture(self.request.FILES['profile_pic'])
            profile_instance.profile_pic_url = profile_pic_url
            profile_instance.save()

    def perform_update(self, serializer):
        profile_instance = serializer.save()
        if 'profile_pic' in self.request.FILES:
            profile_pic_url = upload_profile_picture(self.request.FILES['profile_pic'])
            profile_instance.profile_pic_url = profile_pic_url
            profile_instance.save()


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
from django.contrib.auth import get_user_model
from .models import  Account
from rest_framework import permissions, viewsets, status
from .serializers import UserSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
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


class UserViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = UserSerializer

    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def register(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def login(self, request):
        username = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def upload_profile_pic(self, request):
        user = request.user
        profile_pic = request.FILES.get('profile_pic')

        if user and profile_pic:
            filename = f"profile_pics/{user.id}_{profile_pic.name}"
            try:
                storage.child(filename).put(profile_pic)
                user.profile_image = storage.child(filename).get_url(None)
                user.save()
                return Response({'message': 'Profile picture uploaded successfully'}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'error': 'User or profile pic file not provided'}, status=status.HTTP_400_BAD_REQUEST)
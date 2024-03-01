from django.contrib.auth.models import Group
from ..models import Event, Account
from rest_framework import permissions, viewsets, status
from .serializers import EventSerializer, UserSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login


class UserViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = UserSerializer

    permission_classes = [permissions.IsAuthenticated]

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

    

# class GroupViewSet(viewsets.ModelViewSet):
#     queryset = Group.objects.all()
#     serializer_class = GroupSerializer

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
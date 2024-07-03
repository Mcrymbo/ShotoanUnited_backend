# from django.contrib.auth.models import Group
from ..models import Event, Message
from rest_framework import viewsets
from .serializers import EventSerializer, MessageSerializer

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
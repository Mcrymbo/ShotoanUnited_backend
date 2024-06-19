from django.contrib.auth.models import Group
from ..models import Event
from rest_framework import viewsets
from .serializers import EventSerializer

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
from rest_framework import serializers
from ..models import Event, Message


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'created_at', 'name', 'venue', 'date', 'description', 'poster_image']
    
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
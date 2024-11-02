from rest_framework import serializers
from ..models import Event, Message


class EventSerializer(serializers.ModelSerializer):
    registration_link = serializers.SerializerMethodField()
    class Meta:
        model = Event
        fields = ['id', 'created_at', 'name', 'venue', 'date', 'slug', 'description', 'poster_image', 'registration_link']

        def get_registration_link(self, obj):
            return f"https://shotokanunitedkenya.org/backend/register/{obj.slug}"
    
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
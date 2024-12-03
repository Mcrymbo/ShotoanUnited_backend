from rest_framework import serializers
from ..models import Event, Message, EventImage

class EventImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventImage
        fields = ['id', 'image', 'image_url']

    def create(self, validated_data):
        """ triggers firebase upload """
        instance = super().create(validated_data)
        instance.save()

        return instance

class EventSerializer(serializers.ModelSerializer):
    posted_by = serializers.CharField(source='posted_by.fullname', read_only=True)
    registration_link = serializers.SerializerMethodField()
    images = EventImageSerializer(many=True, required=False)
    class Meta:
        model = Event
        fields = ['id', 'created_at', 'title', 'venue',
                  'date', 'posted_by', 'description', 'content', 'images',
                  'registration_link']

    def create(self, validated_data):
        """ used to create news with multiple images """
        images_data = validated_data.pop("images", [])
        news_instance = Event.objects.create(**validated_data)

        for image in images_data:
            EventImage.objects.create(news=news_instance, **image)

        return news_instance

    def update(self, instance, validated_data):
        """ handles updating News with nested images """
        images_data = validated_data.pop("images", [])
        instance = super().update(instance, validated_data)

        if images_data is not None:
            instance.images.all().delete()
            for image in images_data:
                EventImage.objects.create(news=instance, **image)

        return instance
    
    def get_registration_link(self, obj):
        return f"https://shotokanunitedkenya.org/register/backend/{obj.slug}"
    
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
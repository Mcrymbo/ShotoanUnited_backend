from rest_framework import serializers
from .models import News

class NewsSerializers(serializers.ModelSerializer):
    registration_link = serializers.SerializerMethodField()
    class Meta:
        model = News
        fields = ['id', 'title', 'slug', 'date', 'created_at', 'description', 'cover_image_url', 'registration_link']
    
    def get_registration_link(self, obj):
        return f"https://shotokanunitedkenya.org/register/{obj.slug}"
from django.shortcuts import render
from .serializers import NewsSerializers
from rest_framework import ViewSets
from accounts.models import storage
from .models import News

# Create your views here.

# helper function to upload cover image
def upload_cover_image(cover_image):
    with cover_image.open() as img:
        storage.child(f"news_cover_images/{cover_image.name}").put(img)
        url = storage.child(f"news_cover_images/{cover_image.name}").get_url(None)
        return url
    
class NewsViewSets(ViewSets.ModelViewSet):
    """ viewset for handling ends points to news """
    queryset = News.objects.all()
    serializer_class = NewsSerializers

    def perform_create(self, serializer):
        news_instance = serializer.save()
        if 'cover_image' in self.request.FILES:
            cover_image_url = upload_cover_image(self.request.FILES['cover_image'])
            news_instance.cover_image_url = cover_image_url
            news_instance.save()
    
    def perform_update(self, serializer):
        news_instance = serializer.save()
        if 'cover_image' in self.request.FILES:
            cover_image_url = upload_cover_image(self.request.FILES['cover_image'])
            news_instance.cover_image_url = cover_image_url
            news_instance.save()
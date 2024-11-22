from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import NewsSerializers, CommentSerializer
from rest_framework import viewsets, status
from accounts.models import storage
from .models import News, Like, Comment
from .signals import create_whatsapp_share_link

# Create your views here.

# helper function to upload cover image
def upload_cover_image(cover_image):
    with cover_image.open() as img:
        storage.child(f"news_cover_images/{cover_image.name}").put(img)
        url = storage.child(f"news_cover_images/{cover_image.name}").get_url(None)
        return url
    
class NewsViewSets(viewsets.ModelViewSet):
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

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.views += 1
            instance.save()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except:
            return Response({"Error": "news not found"}, status=404)

    @action(detail=True, methods=["post"])
    def increment_views(self, request, pk=None):
        try:
            news = News.objects.get(pk=pk)
            news.views += 1
            news.save()

            return Response({"message": "added a view", "views": news.views}, status=status.HTTP_202_CREATED)
        except News.DoesNotExist:
            return Response({"Error": "news item not found"}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['get'])
    def get_views(self):
        try:
            news = News.objects.get(pk=pk)
            return Response({"views": news.views}, status=status.HTTP_200)
        except News.DoesNotExist:
            return Response({"Error": "news item not found"}, status=status.HTTP_404_NOT_FOUND)



class LikeNewsView(APIView):

    def post(self, request, pk):
        news = News.objects.get(pk=pk)
        like, created = Like.objects.get_or_create(user=request.user, news=news)

        if not created:
            like.delete()
            return Response({"message": "unliked news"}, status=200)
        return Response({"message": "liked news"}, status=201)

class CommentsNewsView(APIView):

    def post(self, request, pk):
        try:
            news = News.objects.get(pk=pk)
        except News.DoesNotExist:
            return Response({"Error": "News does not exists"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CommentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user, news=news)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)

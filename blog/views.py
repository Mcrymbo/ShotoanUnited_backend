from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db import transaction
from django.db.models import F
from .models import Blog, Blog_Like, Category
from .serializers import BlogSerializer, CommentSerializer, CategorySerializer

class BlogViewSets(viewsets.ModelViewSet):
    """ViewSet for handling endpoints related to news"""
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

    @action(detail=True, methods=["post"])
    def increment_views(self, request, pk=None):
        """Increment the view count for a news item"""
        updated = Blog.objects.filter(pk=pk).update(views=F("views") + 1)
        if updated:
            news = Blog.objects.get(pk=pk)
            return Response({"message": "Added a view", "views": news.views}, status=status.HTTP_202_ACCEPTED)
        return Response({"Error": "News item not found"}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['get'])
    def get_views(self, request, pk=None):
        """Retrieve the view count for a news item"""
        try:
            news = Blog.objects.get(pk=pk)
            return Response({"views": news.views}, status=status.HTTP_200_OK)
        except Blog.DoesNotExist:
            return Response({"Error": "News item not found"}, status=status.HTTP_404_NOT_FOUND)


class LikeNewsView(APIView):
    """API View for liking/unliking a news item"""
    permission_classes = [AllowAny]

    def post(self, request, pk=None):
        try:
            news = Blog.objects.get(pk=pk)
        except Blog.DoesNotExist:
            return Response({"Error": "News item not found"}, status=status.HTTP_404_NOT_FOUND)

        session_id = request.session.session_key
        if not session_id:
            request.session.create()
            session_id = request.session.session_key

        with transaction.atomic():
            try:
                if request.user.is_authenticated:
                    like = Blog_Like.objects.get(user=request.user, blog=news)
                else:
                    like = Blog_Like.objects.get(session_id=session_id, blog=news)
                like.delete()
                news.likes_count = max(news.likes_count - 1, 0)
                news.save(update_fields=['likes_count'])
                return Response({"message": "Unliked the news", "likes_count": news.likes_count}, status=status.HTTP_200_OK)
            except Blog_Like.DoesNotExist:
                Blog_Like.objects.create(
                    user=request.user if request.user.is_authenticated else None,
                    session_id=session_id,
                    blog=news
                )
                news.likes_count += 1
                news.save(update_fields=['likes_count'])
                return Response({"message": "Liked the news", "likes_count": news.likes_count}, status=status.HTTP_201_CREATED)


class CommentsNewsView(APIView):
    """API View for handling comments on a news item"""
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            news = Blog.objects.get(pk=pk)
        except Blog.DoesNotExist:
            return Response({"Error": "News does not exist"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, news=news)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoryViewsets(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
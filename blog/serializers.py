from rest_framework import serializers
from .models import Blog, BlogImage, Blog_Comment, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog_Comment
        fields = '__all__'

class BlogImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogImage
        fields = "__all__"
    
    def create(self, validated_data):
        """ triggers firebase upload """
        instance = super().create(validated_data)
        instance.save()

        return instance
    
class BlogSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.fullname', read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    images = BlogImageSerializer(many=True, required=False)

    class Meta:
        model = Blog
        fields = ['id', 'title', 'excerpt', 'slug',
                  'created_at', 'views',
                  'author',
                  'comments', 'images']
    
    def create(self, validated_data):
        """ used to create news with multiple images """
        images_data = validated_data.pop("images", [])
        news_instance = Blog.objects.create(**validated_data)

        for image in images_data:
            BlogImage.objects.create(news=news_instance, **image)

        return news_instance
    
    def update(self, instance, validated_data):
        """ handles updating News with nested images """
        images_data = validated_data.pop("images", [])
        instance = super().update(instance, validated_data)

        if images_data is not None:
            instance.images.all().delete()
            for image in images_data:
                BlogImage.objects.create(news=instance, **image)

        return instance
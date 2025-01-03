from rest_framework import serializers
from .models import News, Like, Comment, NewsImage, Category


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'user', 'content', 'created_at']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class NewsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsImage
        fields = ['id', 'image', 'image_url']

    def create(self, validated_data):
        """ triggers firebase upload """
        instance = super().create(validated_data)
        instance.save()

        return instance


class NewsSerializers(serializers.ModelSerializer):
    registration_link = serializers.SerializerMethodField()
    author = serializers.CharField(source='author.fullname', read_only=True)
    # comments = CommentSerializer(many=True, read_only=True)
    images = NewsImageSerializer(many=True, required=False)
    category = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = News
        fields = ['id', 'title', 'slug', 'date', 'is_featured',
                  'created_at', 'description', 'is_trending',
                  'registration_link', 'author', 'content',
                  "category", 'images']

    def create(self, validated_data):
        """ used to create news with multiple images """
        images_data = validated_data.pop("images", [])
        news_instance = News.objects.create(**validated_data)

        for image in images_data:
            NewsImage.objects.create(news=news_instance, **image)

        return news_instance

    def update(self, instance, validated_data):
        """ handles updating News with nested images """
        images_data = validated_data.pop("images", [])
        instance = super().update(instance, validated_data)

        if images_data is not None:
            instance.images.all().delete()
            for image in images_data:
                NewsImage.objects.create(news=instance, **image)

        return instance
                                     
    
    def get_registration_link(self, obj):
        return f"https://shotokanunitedkenya.org/register/{obj.slug}"

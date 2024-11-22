from django.db import models
from django.core.files.base import ContentFile
from uuid import uuid4
from django.utils.text import slugify
from accounts.models import storage, Account
from django.conf import settings


# Create your models here.
class News(models.Model):
    """ Model for News """

    class Meta:
        ordering = ['created_at']

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    title = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, blank=True, default="")
    date = models.DateField(verbose_name='target date')
    created_at = models.DateField(verbose_name='date created', auto_now_add=True)
    updated_at = models.DateField(verbose_name='date updated', auto_now=True)
    description = models.TextField(max_length=300)
    author = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True)    
    content = models.TextField(null=True, blank=True)

    views = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        """ save slug """
        
        if not self.slug:
            self.slug = slugify(f"{self.title}-{uuid4().hex[:8]}")
        
        super().save(*args, **kwargs)
    
    def get_registration_link(self):
        return f"https://shotokanunitedkenya.org/register/{self.slug}"
    
    @property
    def likes(self):
        return self.likes.count()

    @property
    def comment_count(self):
        return self.comments.count()


class NewsImage(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    news = models.ForeignKey(News, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='news_images', blank=True, null=True)
    image_url = models.CharField(max_length=200, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.image:
            image_file = self.image.file
            file_name = self.image.name
            file_content = ContentFile(image_file.read())

            storage.child(f"news_images/{file_name}").put(file_content)
            self.image_url = storage.child(f"news_images/{file_name}").get_url(None)

            self.image = None

        super().save(*args, **kwargs)


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    news = models.ForeignKey('News', on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'news')

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    news = models.ForeignKey('News', on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user} on {self.news.title}"

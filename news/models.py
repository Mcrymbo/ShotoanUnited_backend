from django.db import models
from django.core.files.base import ContentFile
from uuid import uuid4
from django.utils.text import slugify
from accounts.models import storage, Account
from django.conf import settings


# Create your models here.
class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.name}-{uuid4().hex[:12]}")
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    

class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    session_id = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'session_id')

    def save(self, *args, **kwargs):
        if self.user:
            if Like.objects.filter(user=self.user, news=self.news).exists():
                return
        else:
            if Like.obkects.filter(session_id=self.session_id, news=self.news).exists():
                return
        super().save(*args, **kwargs)

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user} on {self.news.title}"



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
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    is_featured = models.BooleanField(default=False)
    is_trending = models.BooleanField(default=False)
    content = models.TextField(null=True, blank=True)
    likes = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True)
    comments = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True)
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
    
    def __str__(self):
        return self.title


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

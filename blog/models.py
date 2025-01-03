from django.db import models
import uuid
from accounts.models import Account
import pyrebase
import environ
from django.utils.text import slugify
from django.core.files.base import ContentFile
from django.conf import settings

# Load environment variables
env = environ.Env()
environ.Env.read_env()

# Initialize Firebase
firebase = pyrebase.initialize_app({
    "apiKey": env('API_KEY'),
    "authDomain": env('AUTH_DOMAIN'),
    "projectId": env('PROJECT_ID'),
    "storageBucket": env('STORAGE_BUCKET'),
    "messagingSenderId": env('MESSAGING_SENDER_ID'),
    "appId": env('APP_ID'),
    "measurementId": env('MEASUREMENT_ID'),
    "databaseURL": ""
})

storage = firebase.storage()

class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return self.name
    

class Blog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    excerpt = models.TextField()
    author = models.ForeignKey(Account, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='blog', null=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.title}-{uuid.uuid4().hex[:8]}")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class BlogImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    blog = models.ForeignKey(Blog, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='news_images', blank=True, null=True)
    image_url = models.CharField(max_length=200, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.image:
            file_name = self.image.name
            file_content = ContentFile(self.image.file.read())

            # Upload to Firebase storage
            storage.child(f"blog_images/{file_name}").put(file_content)
            self.image_url = storage.child(f"blog_images/{file_name}").get_url(None)

            self.image = None  # Avoid saving the image locally

        super().save(*args, **kwargs)

class Blog_Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, null=True, blank=True)
    session_id = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'session_id')

    def save(self, *args, **kwargs):
        if self.user:
            if Blog_Like.objects.filter(user=self.user, news=self.news).exists():
                return
        else:
            if Blog_Like.obkects.filter(session_id=self.session_id, news=self.news).exists():
                return
        super().save(*args, **kwargs)

class Blog_Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user} on {self.blog.title}"
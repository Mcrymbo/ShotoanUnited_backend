from django.db import models
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.utils.text import slugify
from accounts.models import storage
import uuid

User = get_user_model()

# Create your models here.
class BaseModel(models.Model):
    """Base Model class where all classes inherit from"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        abstract = True

class Event(BaseModel):
    """ creates events model """
    title = models.CharField(max_length=200)
    venue = models.CharField(max_length=200)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField()
    slug = models.SlugField(unique=True, blank=True, default="")
    description = models.TextField(max_length=250, blank=True, null=True)
    content = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.title}-{uuid.uuid4().hex[:8]}")
        super().save(*args, **kwargs)
    
    def get_registration_link(self):
        return f"https://shotokanunitedkenya.org/register/backend/{self.slug}"

    def __str__(self):
        return self.title

class EventImage(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event = models.ForeignKey(Event, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='event_images', blank=True, null=True)
    image_url = models.CharField(max_length=200, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.image:
            image_file = self.image.file
            file_name = self.image.name
            file_content = ContentFile(image_file.read())

            storage.child(f"event_images/{file_name}").put(file_content)
            self.image_url = storage.child(f"event_images/{file_name}").get_url(None)

            self.image = None

        super().save(*args, **kwargs)
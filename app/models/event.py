from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
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
    name = models.CharField(max_length=200)
    venue = models.CharField(max_length=200)
    date = models.DateField()
    slug = models.SlugField(unique=True, blank=True, default="")
    description = models.TextField()
    poster_image = models.ImageField(upload_to='images/poster_images/', null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.name}-{uuid.uuid4().hex[:8]}")
        super().save(*args, **kwargs)
    
    def get_registration_link(self):
        return f"https://shotokanunitedkenya.org/backend/register/{self.slug}"

    def __str__(self):
        return self.name
from django.db import models
from django.contrib.auth import get_user_model
import uuid
from accounts.models import Account

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
    description = models.TextField()
    poster_image = models.ImageField(upload_to='images/poster_images/', null=True, blank=True)


    def __str__(self):
        return self.name
from django.db import models
import uuid
from accounts.models import Account


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

class Message(BaseModel):
    """ records the inquiry from general public """
    name = models.CharField(max_length=30, blank=False)
    email = models.EmailField(verbose_name='email', max_length=60, blank=False)
    message = models.TextField(max_length=300, blank=False)
    reply_by = models.OneToOneField(Account, on_delete=models.CASCADE, blank=True, null=True)
    reply = models.TextField(max_length=400, blank=True, null=True)
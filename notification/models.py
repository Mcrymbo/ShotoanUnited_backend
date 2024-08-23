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


class Message(BaseModel):
    """ records the inquiry from general public """
    name = models.CharField(max_length=30, blank=False)
    email = models.EmailField(verbose_name='email', max_length=60, blank=False)
    message = models.TextField(max_length=300, blank=False)
    reply_by = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    reply = models.TextField(max_length=400, blank=True, null=True)
    notification_sent = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.name} ({self.email})"

    class Meta:
        ordering = ['-created_at']

class Notification(models.Model):
    """ Model for pushing notifications """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_notification")
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="message_notification")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.email}"

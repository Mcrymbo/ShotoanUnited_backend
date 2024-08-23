from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Notification, Message

@receiver(post_save, sender=Message)
def create_message_notification(sender, instance, created, **kwargs):
    if created:
        # Notification for a new message
        Notification.objects.create(
            user=instance.reply_by,  # Notify the assigned user (if any)
            message=instance,
            content=f"New inquiry from {instance.name} ({instance.email})."
        )
    elif instance.reply and not instance.notification_sent:
        # Notification for a reply
        Notification.objects.create(
            user=instance.reply_by,  # Notify the user who replied
            message=instance,
            content=f"Your inquiry has been replied to by {instance.reply_by.username}."
        )
        instance.notification_sent = True
        instance.save()
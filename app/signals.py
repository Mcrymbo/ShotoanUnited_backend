from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Event

@receiver(post_save, sender=Event)
def create_whatsapp_share_link(sender, instance, created, **kwargs):
    if created:
        registration_link = instance.get_registration_link()
        print(f"WhatsApp Share Link: https://wa.me/?text=Register%20for%20{instance.title}%20at%20{registration_link}")
from django.db import models
from django.core.files.base import ContentFile
from uuid import uuid4
from accounts.models import storage


# Create your models here.
class News(models.Model):
    """ Model for News """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    title = models.CharField(max_length=50)
    date = models.DateField(verbose_name='target date')
    created = models.DateField(verbose_name='date created', auto_now_add=True)
    updated = models.DateField(verbose_name='date updated', auto_now=True)
    description = models.TextField(max_length=300)
    cover_image = models.ImageField(upload_to='news_cover', blank=True, null=True)
    cover_image_url = models.CharField(max_length=200, blank=True, null=True)

    def save(self, *args, **kwargs):
        """ save cover image to firebase """
        if self.cover_image and hasattr(self.cover_image_url, 'file'):
            cover_image_file = self.cover_image.file
            file_name = self.cover_image.name
            file_content = ContentFile(cover_image_file.read())

            storage.child(f"news_cover_images/{file_name}").put(file_content)
            cover_image_url = storage.child(f"news_cover_images/{file_name}").get_url(None)

            # Update the profile_pic_url field with the URL
            self.cover_image_url = cover_image_url

            self.cover_image = None
        
        super().save(*args, **kwargs)
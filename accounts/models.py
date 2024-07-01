import uuid
from django.core.files.base import ContentFile
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import pyrebase
import environ

env = environ.Env()
environ.Env.read_env()

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

class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, first_name=None, last_name=None, password=None):
        if not email:
            raise ValueError("User must have an email.")
        if not username:
            raise ValueError("User must have a username")
        
        user = self.model(
            email=self.normalize_email(email.lower()),
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username, first_name=None, last_name=None, password=None):
        user = self.create_user(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(verbose_name='email', max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now_add=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    profile_image = models.CharField(max_length=255, null=True, blank=True, default='')
    hide_email = models.BooleanField(default=True)
    is_deactivated = models.BooleanField(default=False)

    objects = MyAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'password']

    def __str__(self):
        return self.username
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return self.is_admin


class Profile(models.Model):
    """ define the profile of a user """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(Account, null=True, on_delete=models.CASCADE)
    club = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=30, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)
    cover_photo= models.ImageField(upload_to='cover_pics', blank=True)
    profile_pic_url = models.URLField(max_length=200, blank=True)
    cover_photo_url = models.URLField(max_length=200, blank=True)

    def save(self, *args, **kwargs):
        # Override save method to upload profile pic to Firebase Storage
        if self.profile_pic and hasattr(self.profile_pic, 'file'):

            profile_pic_file = self.profile_pic.file
            file_name = self.profile_pic.name
            file_content = ContentFile(profile_pic_file.read())

            storage.child(f"profile_pics/{file_name}").put(file_content)
            profile_pic_url = storage.child(f"profile_pics/{file_name}").get_url(None)

            # Update the profile_pic_url field with the URL
            self.profile_pic_url = profile_pic_url

            self.profile_pic = None
        
        if self.cover_photo and hasattr(self.cover_photo, 'file'):

            cover_photo_file = self.cover_photo.file
            file_name = self.cover_photo.name
            file_content = ContentFile(cover_photo_file.read())

            storage.child(f"cover_photo/{file_name}").put(file_content)
            cover_photo_url = storage.child(f"cover_photo/{file_name}").get_url(None)

            # Update the profile_pic_url field with the URL
            self.cover_photo_ur =  cover_photo_url

            self.cover_photo_ur = None

        super().save(*args, **kwargs)
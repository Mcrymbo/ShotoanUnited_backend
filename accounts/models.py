import uuid
from django.core.files.base import ContentFile
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
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
    def create_user(self, email, first_name=None, last_name=None, password=None):
        if not email:
            raise ValueError("User must have an email.")
        
        user = self.model(
            email=self.normalize_email(email.lower()),
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, first_name=None, last_name=None, password=None):
        user = self.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractUser):
    """ Defines custom user """

    ADMIN1 = 1
    ADMIN2 = 2
    ADMIN3 = 3
    GUEST = 4

    ROLES = [
        (ADMIN1, 'Admin1'),
        (ADMIN2, 'Admin2'),
        (ADMIN3, 'Admin3'),
        (GUEST, 'Guest'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(verbose_name='email', max_length=60, unique=True)
    username = None
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    fullname = models.CharField(max_length=250, blank=True, null=True)
    role = models.PositiveSmallIntegerField(choices=ROLES, default=GUEST)
    profile_image = models.CharField(max_length=255, null=True, blank=True, default='')
    hide_email = models.BooleanField(default=True)
    is_deactivated = models.BooleanField(default=False)

    objects = MyAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name',]

    def __str__(self):
        return self.fullname
    
    def has_perm(self, perm, obj=None):
        return self.is_staff
    
    def has_module_perms(self, app_label):
        return self.is_staff
    
    @property
    def fullname(self):
        return f"{self.first_name or ''} {self.last_name or ''}".strip()


class Profile(models.Model):
    """ define the profile of a user """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(Account, null=True, on_delete=models.CASCADE)
    club = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=30, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)
    cover_photo= models.ImageField(upload_to='cover_pics', blank=True)
    profile_pic_url = models.URLField(max_length=200, blank=True)
    cover_photo_url = models.URLField(max_length=200, blank=True, null=True)
    bio = models.TextField(max_length=300, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

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
            self.cover_photo_url =  cover_photo_url

            self.cover_photo = None

        super().save(*args, **kwargs)

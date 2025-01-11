from django.db import models
from accounts.models import Account
import uuid

# Create your models here.
class Coach(Account):
    certifications = models.TextField()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = 2
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'coaches'


class Dojo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=250)
    coach = models.ForeignKey(Coach, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name
    
class Player(Account):
    dojo = models.ForeignKey(Dojo, on_delete=models.CASCADE, null=True, blank=True)
    belt_rank = models.CharField(max_length=250)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = 3
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'players'

class RegistrationToken(models.Model):
    user_type_choices = [
        ('coach', 'Coach'),
        ('player', 'Player'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    user_type = models.CharField(choices=user_type_choices, max_length=10)
    dojo = models.ForeignKey('Dojo', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user_type} - {self.token}"
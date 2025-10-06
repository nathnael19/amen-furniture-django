from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True,)
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    phone = models.CharField(max_length=10,unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','phone','first_name','last_name']

    def __str__(self):
        return self.username
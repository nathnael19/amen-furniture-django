from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager
import uuid
# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True,)
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    phone = models.CharField(max_length=10,unique=True,null=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','phone','first_name','last_name']

    objects = UserManager()

    def __str__(self):
        return self.username


class Address(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="address")
    address = models.CharField(max_length=255)
    is_default = models.BooleanField(default=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user} {self.address}'
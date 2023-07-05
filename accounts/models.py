from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Member(AbstractUser):
    age = models.IntegerField(verbose_name="나이",default=10, null=True)
    id = models.AutoField(primary_key=True)
from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Authority(models.Model):
    # major = models.CharField(max_length=10)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    administrator = models.BooleanField(default=False)
    write = models.BooleanField(default=False)
    read = models.BooleanField(default=True)


class Sex(models.Model):
    sex = models.CharField(max_length=1)

    def __str__(self):
        return self.sex


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.CharField(max_length=20, default="未知")
    sex = models.BooleanField(default=False)  # True is male

    def __str__(self):
        return self.user.username

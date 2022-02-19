from django.db import models

from django.contrib.auth.models import AbstractUser


# s ovim smo upravo uhvatili clasu User orginalnu i sad ide modifikacija (kada zelis to raditi ne zaboravi u settigns dodati AUTH_USER_MODEL)
class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True)
    bio = models.TextField(null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    picture = models.ImageField(upload_to='profile_images', blank = True)

    def __str__(self):
        return self.user.username

class Group(models.Model):
    pass

class Comment(models.Model):
    pass

class Log(models.Model):
    pass

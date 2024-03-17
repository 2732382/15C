from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    picture = models.ImageField(upload_to='profile_images', blank = True)

    def __str__(self):
        return self.user.username

class Group(models.Model):
    name = models.CharField(max_length=255)
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_date = models.DateField()
    icon = models.ImageField(upload_to='group_icons', blank=True)
    activities = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    announcements = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Comment(models.Model):
    pass

class Log(models.Model):
    pass

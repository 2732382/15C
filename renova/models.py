from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    picture = models.ImageField(upload_to='profile_images', blank = True)

    def __str__(self):
        return self.user.username


class Group(models.Model):
    name = models.CharField(max_length=255, unique=True)
    admin = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    creation_date = models.DateField(default=timezone.now)
    icon = models.ImageField(upload_to='group_icons', blank=True)
    activities = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    announcements = models.TextField(blank=True)
    slug = models.SlugField(unique = True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        super(Group, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Comment(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    creation_date = models.DateField(default=timezone.now)
    likes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.text

class Activity(models.Model):
    name = models.CharField(max_length=200)
    duration = models.IntegerField()

    def __str__(self):
        return self.name


class Log(models.Model):
    creation_date = models.DateField(default=timezone.now)
    activities = models.ManyToManyField(Activity)
    total_duration = models.IntegerField(default=0)
    water = models.IntegerField(default=0)
    calories = models.IntegerField(default=0)
    sleep = models.IntegerField(default=0)

    def __str__(self):
        return str(self.pk)
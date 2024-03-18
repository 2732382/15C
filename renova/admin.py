from django.contrib import admin
from renova.models import UserProfile, Group, Log

admin.site.register(UserProfile)
admin.site.register(Group)
admin.site.register(Log)
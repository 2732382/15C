from django.contrib import admin
from renova.models import *

admin.site.register(UserProfile)
admin.site.register(Group)
admin.site.register(Comment)
admin.site.register(Activity)
admin.site.register(Log)
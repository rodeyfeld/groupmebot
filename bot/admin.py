from django.contrib import admin
from .models import Bot, GroupMember, MediaFile

admin.site.register(Bot)
admin.site.register(GroupMember)
admin.site.register(MediaFile)
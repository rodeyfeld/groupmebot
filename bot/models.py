from django.db import models


class Bot(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    groupme_bot_id = models.CharField(max_length=30)
    groupme_group_id = models.CharField(max_length=10)


class MediaFile(models.Model):
    bot = models.ForeignKey('Bot', null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True)
    search_term = models.CharField(max_length=100, blank=True)
    url = models.CharField(max_length=200, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)


class GroupMember(models.Model):
    bot = models.ForeignKey('Bot', null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True)
    groupme_user_id = models.CharField(max_length=25, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_moderator = models.BooleanField(default=False)

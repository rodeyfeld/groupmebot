from django.db import models


class Bot(models.Model):
    name = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)
    groupme_bot_id = models.CharField(max_length=30)
    groupme_group_id = models.CharField(max_length=10)


class MediaFile(models.Model):
    bot = models.ForeignKey('Bot', null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True)
    search_term = models.CharField(max_length=100, blank=True)
    url = models.CharField(max_length=200, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
from django.db import models

class Bot(models.Model):
    name = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)
    groupme_bot_id = models.CharField(max_length=30)
    groupme_group_id = models.CharField(max_length=10)
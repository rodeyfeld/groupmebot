from django.shortcuts import render
from django.http import HttpResponse
from .models import Bot
# import requests
import os

def index(request):
    return HttpResponse("Bot listener index")

def bot(request, groupme_bot_id):
    bot = Bot.objects.get(groupme_bot_id=groupme_bot_id)
    bot_name = bot.name
    return HttpResponse("Bot page for %s" % bot_name)

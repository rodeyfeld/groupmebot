from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from .models import Bot
import requests
import os

def index(request):
    return HttpResponse("Bot listener index")

def bot(request, groupme_bot_id):
    bot = Bot.objects.get(groupme_bot_id=groupme_bot_id)
    bot_name = bot.name
    request_params = {
        'token': settings.GROUPME_API_KEY
    }

    get_messages(bot, request_params)

    return HttpResponse("Bot page for %s" % bot_name)

def get_messages(bot, request_params):
    groupme_group_id = bot.groupme_group_id
    response_messages = requests.get('https://api.groupme.com/v3/groups/' + groupme_group_id + '/messages', params = request_params).json()['response']['messages']
    print(response_messages)

    

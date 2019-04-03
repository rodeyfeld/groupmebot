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
    print(request.body)
    # print request.POST.get
    get_message(bot, request_params)

    return HttpResponse("Bot page for %s" % bot_name)

def get_message(bot, request_params):
    groupme_group_id = bot.groupme_group_id
    try:
        response_messages = requests.get('https://api.groupme.com/v3/groups/' + groupme_group_id + '/messages', params = request_params).json()['response']['messages']
        most_recent_response = response_messages[0]
        if is_bot_command(most_recent_response):
            print("Bot has recieved a message")
        else:
            print("User or bot has sent a message")
    except:
        print("It failed bad")
def is_bot_command(response):
    message = response['text']
    sender_type = response['sender_type']
    if message[0] == '!' and sender_type != 'system':
        return True



    

from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings

from .commands import giphy
from .models import Bot
import requests
import os


def index(request):
    return HttpResponse("Bot listener index")


def bot_reciever(request, groupme_bot_id):
    bot = Bot.objects.get(groupme_bot_id=groupme_bot_id)
    bot_name = bot.name
    request_params = {
        'token': settings.GROUPME_API_KEY
    }
    get_message(bot, request_params)
    # test_message(bot, request_params)
    return HttpResponse("Bot page for %s" % bot_name)


def get_message(bot, request_params):
    groupme_group_id = bot.groupme_group_id
    try:
        response_messages = requests.get('https://api.groupme.com/v3/groups/' + groupme_group_id + '/messages',
                                         params=request_params).json()['response']['messages']
        # most_recent_response = response_messages[0]
        most_recent_response = {'text': "!gif orca", 'sender_type': "user"}
        print(most_recent_response)
        if is_bot_command(most_recent_response):
            print("Bot has received a message")
            process_command(bot, most_recent_response['text'])
        else:
            print("User or bot has sent a message")
            process_response(bot, most_recent_response)
    except Exception as e:
        print(e)
        pass


def is_bot_command(response):
    message = response['text']
    sender_type = response['sender_type']
    if message[0] == '!' and sender_type != 'system':
        return True


def process_command(bot, message_response):
    command_tokens = message_response.split()
    command = command_tokens[0].replace('!', '').upper()
    args = command_tokens[1:]
    if command == 'GIF':
        giphy.send_giphy(bot=bot, search_term=' '.join(args))


def process_response(bot, message_response):
    return True



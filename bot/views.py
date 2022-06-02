from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from .commands import giphy, lotr, event
from .models import Bot, GroupMember
import requests
import os


def index(request):
    return HttpResponse("Bot listener index")


@csrf_exempt
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
        most_recent_response = response_messages[0]
        if is_bot_command(most_recent_response):
            print("Bot has received a message")
            process_command(bot=bot, most_recent_response=most_recent_response)
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


def process_command(bot, most_recent_response):
    groupme_user_id = most_recent_response['user_id']
    groupmember, created = GroupMember.objects.get_or_create(bot=bot, groupme_user_id=groupme_user_id)
    groupmember.name = most_recent_response['name']
    groupmember.save()
    message_text = most_recent_response['text']
    command_tokens = message_text.split()
    command = command_tokens[0].replace('!', '').upper()
    args = command_tokens[1:]

    if command == 'DEACTIVATE' and groupmember.is_moderator:
        bot.is_active = False
        request_params = {'bot_id': bot.groupme_bot_id, 'text': 'Bot has been deactivated'}
        requests.post('https://api.groupme.com/v3/bots/post', params=request_params)
        bot.save()
    elif command == 'ACTIVATE' and groupmember.is_moderator:
        bot.is_active = True
        request_params = {'bot_id': bot.groupme_bot_id, 'text': 'Bot has been activated'}
        requests.post('https://api.groupme.com/v3/bots/post', params=request_params)
        bot.save()
    if bot.is_active:
        if command == 'KNIGHT' and groupmember.is_admin:
            try:
                search_name = ' '.join(args)[1:]
                search_groupmember = GroupMember.objects.get(bot=bot, name=search_name)
                search_groupmember.is_moderator = True
                search_groupmember.save()
                request_params = {'bot_id': bot.groupme_bot_id, 'text': search_name + ' has been knighted'}
                requests.post('https://api.groupme.com/v3/bots/post', params=request_params)
            except Exception as e:
                request_params = {'bot_id': bot.groupme_bot_id, 'text': 'Could not find groupmember' + search_name}
                requests.post('https://api.groupme.com/v3/bots/post', params=request_params)
                pass
        elif command == 'OUST' and groupmember.is_admin:
            try:
                search_name = ' '.join(args)[1:]
                search_groupmember = GroupMember.objects.get(bot=bot, name=search_name)
                search_groupmember.is_moderator = False
                search_groupmember.save()
                request_params = {'bot_id': bot.groupme_bot_id, 'text': search_name + ' has been ousted'}
                requests.post('https://api.groupme.com/v3/bots/post', params=request_params)
            except Exception as e:
                request_params = {'bot_id': bot.groupme_bot_id, 'text': 'Could not find groupmember' + search_name}
                requests.post('https://api.groupme.com/v3/bots/post', params=request_params)
                pass
        elif command == 'GIF':
            giphy.send_giphy(bot=bot, search_term=' '.join(args))
        elif command == 'LOTRQ':
            lotr.send_lotrq(bot=bot, search_args=args)
        elif command == 'EVENT':
            event.send_event(bot=bot)



def process_response(bot, message_response):
    return True

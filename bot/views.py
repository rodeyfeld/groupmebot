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
    print(bot_name)
    request_params = {
        'token': settings.GROUPME_API_KEY
    }
    get_message(bot, request_params)
    # test_message(bot, request_params)
    return HttpResponse("Bot page for %s" % bot_name)

def test_message(bot, request_params):
    most_recent_response = "!gif super saiyan"
    process_command(bot, most_recent_response)

def get_message(bot, request_params):
    groupme_group_id = bot.groupme_group_id
    try:
        response_messages = requests.get('https://api.groupme.com/v3/groups/' + groupme_group_id + '/messages', params = request_params).json()['response']['messages']
        most_recent_response = response_messages[0]
        print(most_recent_response)
        if is_bot_command(most_recent_response):
            print("Bot has recieved a message")
            process_command(bot, most_recent_response['text'])
        else:
            print("User or bot has sent a message")
            process_response(bot, most_recent_response)
    except:
        print("It failed bad")

def is_bot_command(response):
    message = response['text']
    sender_type = response['sender_type']
    print(message)
    print(sender_type)
    if message[0] == '!' and sender_type != 'system':
        return True

def process_command(bot, message_response):
    print(message_response)
    command_tokens = message_response.split()
    print(command_tokens)
    command = command_tokens[0].replace('!', '').upper()
    print(command)
    args = command_tokens[1:]
    print(command_tokens)
    print(command)
    print(args)
    if command == 'GIF':
        send_image_message(bot, ' '.join(args))


def process_response(bot, message_response):
    return True

def get_giphy_image_url(search_term):
    response = requests.get('https://api.giphy.com/v1/gifs/search', params={'api_key': os.environ.get('GIPHY_API_KEY', ''), 'q': search_term, 'limit': 1})
    print(response.content)
    giphy_image_url = response.json()['data'][0]['images']['original']['url']
    return giphy_image_url

def save_temp_image(url):
    print(url)
    response = requests.get(url, stream=True)
    dirname = os.path.dirname(__file__)
    fpath = os.path.join(dirname, 'tmp')
    fname = "tmp.gif"
    write_path = os.path.join(fpath, fname)
    with open(write_path, 'wb') as writer:
        for chunk in response:
            writer.write(chunk)

def get_image_service_url():
    dirname = os.path.dirname(__file__)
    fpath = os.path.join(dirname, 'tmp')
    fname = "tmp.gif"
    read_path = os.path.join(fpath, fname)
    with open(read_path, 'rb') as reader:
        reader_data = reader.read()
    response = requests.post(url='https://image.groupme.com/pictures', data=reader_data, headers={'Content-Type': 'image/gif', 'X-Access-Token': os.environ.get('GROUPME_API_KEY', '')})
    print(response)
    print(response.content)
    url = response.json()['payload']['url']
    return url

def send_image_message(bot, search_term):
    groupme_bot_id = bot.groupme_bot_id
    giphy_image_url = get_giphy_image_url(search_term)
    save_temp_image(giphy_image_url)
    image_service_url = get_image_service_url()
    request_params = {'bot_id': groupme_bot_id, 'picture_url': image_service_url}
    response = requests.post('https://api.groupme.com/v3/bots/post', params = request_params)
    return response

    

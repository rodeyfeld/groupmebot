import csv
import os
import random
import re

import requests
from django.conf import settings


def send_event(bot):
    print(bot.groupme_bot_id)
    if bot.groupme_bot_id == '6b8b4c8c1922a707fa53e5c4c0':
        quote_string = f"https://goo.gl/maps/cqUnVWxayqHiqBT68"
        request_params = {'bot_id': bot.groupme_bot_id, 'text': re.sub(r'\s+', ' ', quote_string)}
        # print(request_params)
        requests.post('https://api.groupme.com/v3/bots/post', params=request_params)

        quote_string = f"Occurs June 24 - June 26"
        request_params = {'bot_id': bot.groupme_bot_id, 'text': re.sub(r'\s+', ' ', quote_string)}
        # print(request_params)
        requests.post('https://api.groupme.com/v3/bots/post', params=request_params)

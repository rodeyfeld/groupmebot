import csv
import os
import random
import re

import requests
from django.conf import settings


def send_event(bot):
    if bot.groupme_bot_id == '86257932':
        quote_string = f"https://goo.gl/maps/cqUnVWxayqHiqBT68"
        request_params = {'bot_id': bot.groupme_bot_id, 'text': re.sub(r'\s+', ' ', quote_string)}
        # print(request_params)
        requests.post('https://api.groupme.com/v3/bots/post', params=request_params)

        quote_string = f"Occurs June 24 - June 26"
        request_params = {'bot_id': bot.groupme_bot_id, 'text': re.sub(r'\s+', ' ', quote_string)}
        # print(request_params)
        requests.post('https://api.groupme.com/v3/bots/post', params=request_params)

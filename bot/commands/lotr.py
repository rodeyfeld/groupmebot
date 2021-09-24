import csv
import os
import random
import re

import requests
from django.conf import settings


# lotrc_path = os.path.join(settings.MEDIA_DIR, 'permanent', 'lotr', 'lotr_characters.csv')

def send_lotrq(bot, search_args):
    lotrq_path = os.path.join(settings.MEDIA_DIR, 'permanent', 'lotr', 'lotr_quotes.csv')
    with open(lotrq_path) as csv_file:
        reader = csv.DictReader(csv_file)
        rows = list(reader)

        if search_args:
            search_term = ' '.join([search_arg.upper() for search_arg in search_args])
            print(search_term)
            rows = [row for row in rows if row['char'] == search_term]
            print(rows)
    total_rows = len(rows)
    random_quote = rows[random.randrange(total_rows)]
    quote_string = f"{random_quote['dialog']} - {random_quote['char']}, {random_quote['movie']}"
    request_params = {'bot_id': bot.groupme_bot_id, 'text': re.sub(r'\s+', ' ', quote_string)}
    # print(request_params)
    requests.post('https://api.groupme.com/v3/bots/post', params=request_params)


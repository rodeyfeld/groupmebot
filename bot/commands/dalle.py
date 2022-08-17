import requests
import os
import json
from ..models import MediaFile
from django.conf import settings


def get_dalle_image(bot, search_term):
    body = {
        "task_type": "text2im",
        "prompt": {
            "caption": search_term,
            "batch_size": 4,
        }
    }

    url = "https://labs.openai.com/api/labs/tasks"
    headers = {
        'Authorization': "Bearer " + os.environ.get('OPENAPI_BEARER_KEY'),
        'Content-Type': "application/json",
    }

    response = requests.post(url, headers=headers, data=json.dumps(body))
    data = response.json()
    print('DATA FROM 1:', data)
    while True:
        url = f"https://labs.openai.com/api/labs/tasks/{data['id']}"
        response = requests.get(url, headers=headers)
        data = response.json()
        print('DATA FROM 2:', data)
        if not response.ok:
            print(f"Request failed with status: {response.status_code}, data: {response.json()}")
            return None
        if data["status"] == "failed":
            print(f"Task failed: {data['status_information']}")
            return None
        if data["status"] == "rejected":
            print(f"Task rejected: {data['status_information']}")
            return None
        if data["status"] == "succeeded":
            print("🙌 Task completed!")
            data_req = data["generations"]["data"]
            break

    if data_req:
        for generation in data_req:
            image_url = generation["generation"]["image_path"]
            dalle_mediafile = MediaFile.objects.create(bot=bot, name=search_term, url=image_url)
            post_to_bot(dalle_mediafile)


def post_to_bot(mediafile):
    dalle_response = requests.get(mediafile.url, stream=True)
    print(dalle_response, dalle_response.status_code)
    fpath = os.path.join(settings.MEDIA_DIR, 'temp_files')
    fname = '_'.join([mediafile.name, str(mediafile.bot.pk), str(mediafile.pk)]) + '.png'
    file_path = os.path.join(fpath, fname)
    with open(file_path, 'wb') as writer:
        for chunk in dalle_response:
            writer.write(chunk)
    file_path = os.path.join(fpath, fname)
    with open(file_path, 'rb') as reader:
        reader_data = reader.read()

    # Post image to the GroupMe image service, allowing it to be posted to the group
    image_service_response = requests.post(url='https://image.groupme.com/pictures', data=reader_data,
                                           headers={'Content-Type': 'image/gif',
                                                    'X-Access-Token': os.environ.get('GROUPME_API_KEY', '')})

    # Get the URL from the image service post
    image_service_url = image_service_response.json()['payload']['url']

    # Post image to the bot's group
    request_params = {'bot_id': mediafile.bot.groupme_bot_id, 'picture_url': image_service_url}
    response = requests.post('https://api.groupme.com/v3/bots/post', params=request_params)
    return response

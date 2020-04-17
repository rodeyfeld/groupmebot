from django.conf import settings
import requests
import os


def post_mediafile_from_url(mediafile):
    # Save image to local disk
    giphy_response = requests.get(mediafile.url, stream=True)
    fpath = os.path.join(settings.MEDIA_DIR, 'temp_files')
    fname = '_'.join([mediafile.name, str(mediafile.bot.pk), str(mediafile.pk)]) + '.gif'
    file_path = os.path.join(fpath, fname)
    with open(file_path, 'wb') as writer:
        for chunk in giphy_response:
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
    if os.path.isfile(file_path):
        os.remove(file_path)
    else:
        print("Error: %s file not found" % file_path)
    return response


def post_mediafile_from_server(mediafile):
    read_path = os.path.join(settings.MEDIA_DIR, 'permanent', mediafile.name)
    with open(read_path, 'rb') as reader:
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

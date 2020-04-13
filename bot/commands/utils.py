import requests
import os


def post_mediafile_from_url(mediafile):
    # Save image to local disk
    giphy_response = requests.get(mediafile.url, stream=True)
    dirname = os.path.dirname(__file__)
    fpath = os.path.join(dirname, 'media', 'tmp')
    fname = '_'.join([mediafile.name, mediafile.bot.pk, mediafile.pk])
    write_path = os.path.join(fpath, fname)
    with open(write_path, 'wb') as writer:
        for chunk in giphy_response:
            writer.write(chunk)
    read_path = os.path.join(fpath, fname)
    with open(read_path, 'rb') as reader:
        reader_data = reader.read()

    # Post image to the GroupMe image service, allowing it to be posted to the group
    image_service_response = requests.post(url='https://image.groupme.com/pictures', data=reader_data,
                                           headers={'Content-Type': 'image/gif',
                                                    'X-Access-Token': os.environ.get('GROUPME_API_KEY', '')})

    # Get the URL from the image service post
    image_service_url = image_service_response.json()['payload']['url']

    # Post image to the bot's group
    request_params = {'bot_id': mediafile.bot.pk, 'picture_url': image_service_url}
    response = requests.post('https://api.groupme.com/v3/bots/post', params=request_params)
    return response


def post_mediafile_from_server(mediafile):
    dirname = os.path.dirname(__file__)
    read_path = os.path.join(dirname, 'media', 'permanent', mediafile.name)
    with open(read_path, 'rb') as reader:
        reader_data = reader.read()
    # Post image to the GroupMe image service, allowing it to be posted to the group
    image_service_response = requests.post(url='https://image.groupme.com/pictures', data=reader_data,
                                           headers={'Content-Type': 'image/gif',
                                                    'X-Access-Token': os.environ.get('GROUPME_API_KEY', '')})

    # Get the URL from the image service post
    image_service_url = image_service_response.json()['payload']['url']

    # Post image to the bot's group
    request_params = {'bot_id': mediafile.bot.pk, 'picture_url': image_service_url}
    response = requests.post('https://api.groupme.com/v3/bots/post', params=request_params)
    return response

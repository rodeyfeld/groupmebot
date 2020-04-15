from .utils import *
from ..models import MediaFile


def get_giphy_image_url(search_term):
    response = requests.get('https://api.giphy.com/v1/gifs/search',
                            params={'api_key': os.environ.get('GIPHY_API_KEY', ''), 'q': search_term, 'limit': 1})
    try:
        giphy_image_url = response.json()['data'][0]['images']['original']['url']
    except Exception as e:
        print(e)
        giphy_image_url = None
    return giphy_image_url


def send_giphy(bot, search_term):
    giphy_image_url = get_giphy_image_url(search_term=search_term)
    # Check if any url is returned for search term
    if giphy_image_url is not None:
        giphy_mediafile = MediaFile.objects.create(bot=bot, name=search_term, url=giphy_image_url)
        post_mediafile_from_url(giphy_mediafile)
    else:
        no_result_mediafile, created = MediaFile.objects.get_or_create(name="no_result.gif", bot=bot)
        print(no_result_mediafile)
        post_mediafile_from_server(no_result_mediafile)

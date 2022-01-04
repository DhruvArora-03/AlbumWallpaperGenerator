from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
import random
from os.path import exists
from os import makedirs
from urllib.request import urlretrieve
from PIL import Image

id = 'ff1b9dbff35a46f3b96b026bc3f36aaa'
secret = '224f04a3e7d34b11b0d45c3165bf02b2'
uri = 'http://collagify.com/verification'
scope = 'user-library-read'
unit_size = 100
dimesions = (1600, 900)
img_dir = 'album_covers/'
img_file_ending = '.jpg'

def collect_urls_from_saved_albums_helper(results, url_set):
    for item in results['items']:
        album = item['album']
        url_set.add(album['images'][0]['url'])

def collect_urls_from_saved_albums(sp):
    urls = set()
    
    results = sp.current_user_saved_albums()
    collect_urls_from_saved_albums_helper(results, urls)

    while results['next']:
        results = sp.next(results)
        collect_urls_from_saved_albums_helper(results, urls)

    return urls

def collect_and_download_subset(album_set):
    subset = set()

    while len(subset) < (dimesions[0] / unit_size) * (dimesions[1] / unit_size):
        subset.add(random.choice(list(album_set)))


    for album_url in subset:
        if (not exists(img_dir + album_url.split('/')[-1] + img_file_ending)):
            urlretrieve(album_url, img_dir + album_url.split('/')[-1] + img_file_ending)

    return subset

def generate_wallpaper(url_set):
    img = Image.new("RGB", dimesions, (0, 0, 0))

    x = 0
    y = 0
    for url in url_set:
        img.paste(Image.open(img_dir + url.split('/')[-1] + img_file_ending).resize((unit_size, unit_size)), (x, y))

        x += unit_size
        if (x > dimesions[0] - unit_size):
            x = 0
            y += unit_size

    img.save('wallpaper.jpg')
    img.show()

sp = Spotify(auth_manager=SpotifyOAuth(client_id=id, client_secret=secret, redirect_uri=uri, scope=scope))

all_album_urls = collect_urls_from_saved_albums(sp)

# ensure that the directory exists
if (not exists(img_dir)):
    makedirs(img_dir)


smaller_set = collect_and_download_subset(all_album_urls)

generate_wallpaper(smaller_set)
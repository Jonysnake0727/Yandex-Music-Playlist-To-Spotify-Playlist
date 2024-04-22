import spotipy
from spotipy.oauth2 import SpotifyOAuth
import yandex_music
import datetime
from termcolor import colored
import json
import os


# Check if config.json exists
if not os.path.isfile('config.json'):
    print("Error: config.json file not found!")
    exit()

# Load credentials from config.json
with open('config.json') as f:
    try:
        config = json.load(f)
    except json.JSONDecodeError as e:
        print("Error: Invalid JSON format in config.json file!")
        exit()

# Check if all necessary keys are present in config.json
required_keys = ['spotify_credentials', 'yandex_token']
for key in required_keys:
    if key not in config:
        print(f"Error: {key} key not found in config.json file!")
        exit()

# Extract credentials from config
SPOTIPY_CLIENT_ID = config['spotify_credentials']['client_id']
SPOTIPY_CLIENT_SECRET = config['spotify_credentials']['client_secret']
SPOTIPY_USERNAME = config['spotify_credentials']['username']
SPOTIPY_REDIRECT_URI = config['spotify_credentials']['redirect_uri']
YANDEX_TOKEN = config['yandex_token']

# Create a Spotify playlist with today's date
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope="playlist-modify-public"))


def current_month(month):
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    return months[month-1]


def playlist_name_create(playlist_type):
    today_year = datetime.datetime.now().strftime("%Y")
    today_month = datetime.datetime.now().strftime("%m")
    today_day = datetime.datetime.now().strftime("%d")
    playlist_name = f"{today_year} {current_month(int(today_month))} {today_day} {playlist_type} playlist"
    return playlist_name


def yandex_playlist_to_spotify(playlist_type):
    playlist_name = playlist_name_create(playlist_type)
    print("What would you like to name the playlist? By default, it will be named: " + playlist_name)
    answer = input("Answer: ")
    if (not answer == ""): playlist_name = answer
    playlist = sp.user_playlist_create(user=SPOTIPY_USERNAME, name=playlist_name, public=True)
    playlist_id = playlist["id"]
    # Get the Yandex.Music playlist of the day
    client = yandex_music.Client(token=YANDEX_TOKEN, language="ru")
    y_playlists = client.users_likes_playlists()
    for y_playlist in y_playlists:
        if y_playlist["playlist"]["title"] == playlist_type:
            track_ids = []
            for track in y_playlist.playlist.fetch_tracks():
                track_now = track.fetch_track()
                artists = track_now.artists_name()
                artist = artists[0]
                title = track_now.title
                track = sp.search(q=format(f"artist:{artist} track:{title}"), limit=10, offset=0, type='track')
                if track["tracks"]["items"]:
                    track_ids += [track["tracks"]["items"][0]["id"]]
                    print(colored(f'Track "{title}" by {artist} found!', 'green'))
                else:
                    print(colored(f'Failed to find track "{title}" by {artist}', 'red'))
            sp.user_playlist_add_tracks(user=SPOTIPY_USERNAME, playlist_id=playlist_id, tracks=track_ids)
            print(f"Playlist '{playlist_name}' successfully created on Spotify and filled with songs from Yandex.Music!")

print("Welcome to the Yandex Music to Spotify song uploader!\nSelect an action by typing a number:\n1. Playlist of the Day\n2. Deja Vu\n3. Premiere")
while True:
    playlist_type = input("Your choice: ")
    if not playlist_type.isdigit():
        print("Error! Please enter digits!")
    else:
        playlist_type = int(playlist_type)
        if (playlist_type < 4 and playlist_type > 0):
            if (playlist_type == 1): playlist_type = "Плейлист дня"
            elif (playlist_type == 2): playlist_type = "Дежавю"
            elif (playlist_type == 3): playlist_type = "Премьера"
            yandex_playlist_to_spotify(playlist_type)
            break
        else:
            print("Error! Please enter a number from 1 to 3!")

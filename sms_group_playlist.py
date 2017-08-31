import spotipy
import spotipy.util as util

from flask import Flask, request
from urllib.parse import urlparse
from decouple import config


TWILIO_ACCOUNT_SID = config('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = config('TWILIO_AUTH_TOKEN')
SPOTIFY_CLIENT_ID = config('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = config('SPOTIFY_CLIENT_SECRET')
SPOTIFY_REDIRECT_URI = config('SPOTIFY_REDIRECT_URI')
SPOTIFY_PLAYLIST_ID = config('SPOTIFY_PLAYLIST_ID')
SPOTIFY_USERNAME = config('SPOTIFY_USERNAME')


def parse_url(url):
    spotify_url = urlparse(url)
    spotify_url = spotify_url.path
    track_id = spotify_url.split('/')[-1]
    return track_id


app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def song_request():
    username = SPOTIFY_USERNAME
    scope = 'playlist-modify-public'

    content = request.form['Body']
    track_id = parse_url(content)
    track_id = 'spotify:track:{}'.format(track_id)
    scope = 'playlist-modify-public'

    token = util.prompt_for_user_token(username, scope, client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET, redirect_uri=SPOTIFY_REDIRECT_URI)

    if token:
        sp = spotipy.Spotify(auth=token)
        sp.trace = False
        results = sp.user_playlist_add_tracks(username, SPOTIFY_PLAYLIST_ID, [track_id])
    else:
        print('Cant get token for {}'.format(username))
    return "Hello World!"


if __name__ == "__main__":
    app.run(debug=True)

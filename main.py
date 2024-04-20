import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from credentials import my_client_id, my_client_secret
from ytmusicapi import YTMusic

ytmusic = YTMusic("oauth.json")
yt_playlist_id = "PLWc3tzTaQV7tIGzHYKhhSPrOm3ec3aVC7"
spotify_playlist_id = '6ZkwfPHoQFEvxtuXf6dUnr'

# Replace these values with your own credentials
client_id = my_client_id
client_secret = my_client_secret

# Initialize Spotipy client with credentials
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Function to retrieve playlist tracks
def get_playlist_tracks(username, playlist_id):
    results = sp.user_playlist_tracks(username, playlist_id)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return tracks

# Extract data from the playlist
playlist_tracks = get_playlist_tracks('', spotify_playlist_id)

# Print track information
for track in playlist_tracks:
    track_name = track['track']['name']
    artists = ", ".join([artist['name'] for artist in track['track']['artists']])
    album = track['track']['album']['name']
    search_results = ytmusic.search(f"{track_name} by {artists} from {album}")
    ytmusic.add_playlist_items(yt_playlist_id, [search_results[1]['videoId']])
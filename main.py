import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from credentials import my_client_id, my_client_secret
from ytmusicapi import YTMusic

ytmusic = YTMusic("oauth.json")
#yt_playlist_id = "PLWc3tzTaQV7tIGzHYKhhSPrOm3ec3aVC7"
spotify_playlist_id = '37i9dQZEVXbMxcczTSoGwZ'
# Initialize Spotipy client with credentials
client_credentials_manager = SpotifyClientCredentials(client_id=my_client_id, client_secret=my_client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_playlist_info(username, playlist_id):
    playlist_info = sp.user_playlist(username, playlist_id)
    return playlist_info

# Function to retrieve playlist tracks
def get_playlist_tracks(username, playlist_id):
    results = sp.user_playlist_tracks(username, playlist_id)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return tracks

existing_playlists = []

def check_duplicate_playlist():
    playlists = ytmusic.get_library_playlists()
    for playlist in playlists:
        playlist_title = playlist['title']
        existing_playlists.append(playlist_title)

def convert_to_ytmusic():
    # Extract data from the playlist
    print("Haetaan playlist nimi...")
    playlist_name = get_playlist_info('', spotify_playlist_id)
    print("Haetaan playlist kappaleet...")
    playlist_tracks = get_playlist_tracks('', spotify_playlist_id)
    total_tracks = len(playlist_tracks)
    check_duplicate_playlist()
    if playlist_name['name'] in existing_playlists:
        print("ÄLÄ PERKELE!")
        quit()
    else:
        yt_playlist_name = ytmusic.create_playlist(playlist_name['name'], '')
        print("Luodaan playlist: ", playlist_name['name'])
        i = 1
        for track in playlist_tracks:
            track_name = track['track']['name']
            artists = ", ".join([artist['name'] for artist in track['track']['artists']])
            search_results = ytmusic.search(f"{track_name} by {artists}")
            if not search_results:
                print(f"Haku {track_name} by {artists} ei tuottanut tuloksia")
            else:
                print(f"[{i}/{total_tracks}] {track_name} by {artists}")
                i += 1
                ytmusic.add_playlist_items(yt_playlist_name, [search_results[1]['videoId']])

convert_to_ytmusic()
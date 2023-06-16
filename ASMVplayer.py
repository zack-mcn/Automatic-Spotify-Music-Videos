import spotipy
from spotipy.oauth2 import SpotifyOAuth
from youtube_search import YoutubeSearch
from imdb import IMDb
import webbrowser

# Set up Spotify API credentials
client_id = 'your_client_id'
client_secret = 'your_client_secret'
redirect_uri = 'http://localhost:8888/callback'  # Can be any valid URL

# Set up Spotify authentication and access token
scope = 'user-read-currently-playing'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope))
current_track = sp.current_user_playing_track()

# Get the currently playing song information
if current_track is not None:
    song_name = current_track['item']['name']
    artist_name = current_track['item']['artists'][0]['name']
    search_query = f'{song_name} {artist_name} official music video'

    # Search for the song on YouTube
    results = YoutubeSearch(search_query, max_results=1).to_dict()

    if results:
        # Get the URL of the first video in the search results
        video_url = f"https://www.youtube.com/watch?v={results[0]['id']}"

        # Check if IMDb entry exists for the music video
        ia = IMDb()
        imdb_results = ia.search_movie(song_name)

        music_video_found = False
        for result in imdb_results:
            if result.get('kind') == 'video' and artist_name.lower() in str(result.get('title')).lower():
                music_video_found = True
                break

        if music_video_found:
            # Open the video in full screen
            webbrowser.open(video_url, new=2, autoraise=True)
        else:
            print("No IMDb entry found for the music video.")
    else:
        print("No official music video found for the currently playing song.")
else:
    print("No song is currently playing on Spotify.")

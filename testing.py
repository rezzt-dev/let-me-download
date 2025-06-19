import typer
import spotipy
import subprocess
from spotipy.oauth2 import SpotifyClientCredentials
from pytube import Search, YouTube
import os
from pathlib import Path
from rich import print

# Configuración de Spotify
SPICETIFY_CLIENT_ID = "c5794b50d8434dcfacb6b048fbee55c5"
SPICETIFY_CLIENT_SECRET = "24f77befd6e646b6b889a1d658cc066b"


#——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
 # init settings | inicializacion de la configuracion de spotify-downloader ->
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=SPICETIFY_CLIENT_ID,
    client_secret=SPICETIFY_CLIENT_SECRET
))


# Función para obtener info de la canción
def get_track_info(spotify_url):
    track = sp.track(spotify_url)
    name = track['name']
    artist = track['artists'][0]['name']
    return f"{name} {artist}"

# Función para buscar y descargar el primer video de YouTube
def search_and_download(query, output_name):
    s = Search(query)
    if not s.results:
        print("No se encontraron resultados.")
        return
    first_result = s.results[0]
    # Intenta obtener el video_id de ambas formas
    try:
        video_id = first_result.video_id
    except AttributeError:
        video_id = first_result['video_id']
    yt_url = f"https://youtube.com/watch?v={video_id}"
    print(f"Descargando desde: {yt_url}")
    downloadVideoFromURL(yt_url)

def get_playlist_tracks(playlist_url):
    playlist_id = playlist_url.split('/')[-1].split('?')[0]
    results = sp.playlist_tracks(playlist_id)
    tracks = []
    for item in results['items']:
        track = item['track']
        name = track['name']
        artist = track['artists'][0]['name']
        tracks.append(f"{name} {artist}")
    return tracks

def download_playlist(playlist_url):
    tracks = get_playlist_tracks(playlist_url)
    for query in tracks:
        print(f"Buscando: {query}")
        search_and_download(query, query)
    print("¡Descarga completa de la playlist!")
    

def _mainRunner(spotify_url: str):
    print("[bold yellow] [*] SPOT-DOWNLOADER - TESTING [/bold yellow]")
    if "playlist" in spotify_url:
        download_playlist(spotify_url)
    else:
        query = get_track_info(spotify_url)
        print(f"Buscando: {query}")
        search_and_download(query, query)
        print("¡Descarga completa!")

if __name__ == "__main__":
    _mainRunner("https://open.spotify.com/playlist/66HbdfDQSyH2tEy5gH5B1l?si=f8a3ca27920640a5")

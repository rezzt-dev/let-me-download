 # import libraries ->
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from libraries.imports import *
from config.configSettings import SPICETIFY_CLIENT_ID, SPICETIFY_CLIENT_SECRET
from model.mediaModel import downloadAudioFromVideo


#——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
 # init settings | inicializacion de la configuracion de spotify-downloader ->
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=SPICETIFY_CLIENT_ID,
    client_secret=SPICETIFY_CLIENT_SECRET
))


#——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
 # function | createPlaylistFolder | crea la carpeta de almacenamiento de la playlist ->
def createPlaylistFolder (inputBaseFolderPath: Path):
  counter = 0

  while True:
    if counter == 0:
      foldername = "spotify-playlist"
    else:
      foldername = f"spotify-playlist-{counter}"
    fullFolderPath = inputBaseFolderPath / foldername
    if not os.path.exists(fullFolderPath):
      return Path(fullFolderPath)
    counter += 1


#——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
 # funtion | getTrackInfo | obtiene la informacion de una URL de Spotify ->
def getTrackInfo (inputSpotifyURL):
  track = sp.track(inputSpotifyURL)
  name = track['name']
  artist = track['artists'][0]['name']
  return f"{name} {artist}"


#——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
 # function | searchDownloadSong | busca y descarga una cancion de Spotify ->
def searchDownloadSong (inputOutputFolder, inputQuery):
  seacher = Search(inputQuery)
  if not seacher.results:
    print("[bold red] [!] ERROR CRITICO: No se encontraron resultados.[bold red]")
    return
  
  firstResult = seacher.results[0]
  try:
    videoId = firstResult.video_id
  except AttributeError:
    videoId = firstResult['video_id']
  youtubeURL = f"https://youtube.com/watch?v={videoId}"
  downloadAudioFromVideo(inputOutputFolder, youtubeURL)


#——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
 # function | getPlaylistTracks | obtiene las canciones de una playlist de spotify ->
def getPlaylistTracks (inputPlaylistURL):
  playlistId = inputPlaylistURL.split('/')[-1].split('?')[0]
  results = sp.playlist_tracks(playlistId)
  playTracks = []

  for item in results["items"]:
    track = item['track']
    name = track['name']
    artist = track['artists'][0]['name']
    playTracks.append(f"{name} {artist}")
  return playTracks
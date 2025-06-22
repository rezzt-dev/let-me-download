 # import libraries ->
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from libraries.imports import *
from model.helpModel import *
from model.mediaModel import *
from model.spotModel import *


#——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
 # function | executeController | ejecuta el controlador de la aplicacion ->
def executeController (inputFileURL, boolVideo: bool, boolAudio: bool):
  subcontainerFolder = Path(createContainerFolder()) / generateDatetimeString()
  downloadedMediaDone = []

  if not subcontainerFolder.exists():
    subcontainerFolder.mkdir(exist_ok=True)

  with open(inputFileURL, 'r') as videosFile:
    linesURL = videosFile.readlines()
    videoURLs = [fileLine.strip() for fileLine in linesURL if fileLine.strip()]
  
  counter = 0
  for videoURL in videoURLs:
    if "open.spotify.com" in videoURL:
      if "playlist" in videoURL:
        playlistFolderPath = createPlaylistFolder(subcontainerFolder)
        if not playlistFolderPath.exists():
          playlistFolderPath.mkdir(exist_ok=True)

        print("[bold yellow] [>] Cargando canciones de la Playlist[/bold yellow]")
        playlistTracks = getPlaylistTracks(videoURL)

        for trackQuery in playlistTracks:
          print(f"[bold white]   => Descargando: {trackQuery}[/bold white]")
          searchDownloadSong(playlistFolderPath, trackQuery)
        
        downloadedMediaDone.append(videoURL)
        print("[bold green]  [+] DONE! Descarga completa de la Playlist.[/bold green]")
      
      else:
        trackQuery = getTrackInfo(videoURL)
        print(f"[bold white] [>] Descargando: {trackQuery}[/bold white]")
        searchDownloadSong(subcontainerFolder, trackQuery)
        downloadedMediaDone.append(videoURL)
        print("[bold green] [+] DONE! Descarga completada.[/bold green]")
      
      continue


    if boolVideo:
      downloadVideoFromURL(subcontainerFolder, videoURL)
    if boolAudio:
      downloadAudioDirectly(subcontainerFolder, videoURL)

    mediaName = extractTitleFromMedia(videoURL)
    if mediaName != None:
      downloadedMediaDone.append(videoURL)
    else:
      counter += 1
      mediaName = f"video-downloaded-{counter}"
      downloadedMediaDone.append(videoURL)
  return downloadedMediaDone
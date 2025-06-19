 # import libraries ->
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from libraries.imports import *
from model.helpModel import *


#——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
 # function | downloadVideoFromURL | descargar un video a traves de la URL del video ->
def downloadVideoFromURL (inputOutputFolder, inputVideoURL):
  downloadPath = inputOutputFolder

  try:
    videoCommand = [
      "yt-dlp",
      "-f", "bestvideo+bestaudio/best",
      "-o", os.path.join(str(downloadPath), "%(title)s.%(ext)s"),
      inputVideoURL,
    ]

    subprocess.run(videoCommand, shell=False, check=False,
                   stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL)
    
    videoTitleCommand = [
      "yt-dlp",
      "--print", "filename",
      "-o", os.path.join(str(downloadPath), "%(title)s.%(ext)s"),
      inputVideoURL
    ]

    outputFilename = subprocess.check_output(videoTitleCommand, text=True).strip()
    outputPath = os.path.join(str(downloadPath), outputFilename)

    if not os.path.exists(outputPath):
      print(f"[bold red] [!] ERROR CRITICO: Archivo no encontrado: {outputPath} [/bold red]")
      outputPath = None
    
  except subprocess.CalledProcessError as ex:
    print(f"[bold red] [!] ERROR CRITICO: {str(ex)} [/bold red]")
    outputPath = None
  except Exception as ex:
    print(f"[bold red] [!] ERROR CRITICO: {str(ex)} [/bold red]")
    outputPath = None
  return outputPath


#——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
# function | downloadAudioFromVideo | descargar el audio de un video a traves de la URL ->
# function | downloadAudioFromVideo | descargar el audio de un video a traves de la URL ->
def downloadAudioFromVideo(inputOutputFolder, inputVideoURL):
  downloadPath = inputOutputFolder
  try:
    downloadVideoPath = str(downloadVideoFromURL(inputOutputFolder, inputVideoURL))
    if not os.path.exists(downloadVideoPath):
      print(f"[bold red] [!] ERROR CRÍTICO: Archivo no encontrado: {downloadVideoPath} [/bold red]")
      return None
    
    base_audio = os.path.splitext(os.path.basename(downloadVideoPath))[0]
    downloadAudioPath, *_ = getUniqueFilename(downloadPath, base_audio, ".mp3")
    
    auxVideo = VideoFileClip(downloadVideoPath)
    auxVideo.audio.write_audiofile(
      downloadAudioPath,
      codec='mp3',
      bitrate='192k',
      ffmpeg_params=['-ar', '44100'],
      logger=None
    )
    auxVideo.close()
    os.remove(downloadVideoPath)
    return downloadAudioPath
    
  except subprocess.CalledProcessError as ex:
    print(f"[bold red] [!] ERROR CRÍTICO: {str(ex)} [/bold red]")
    return None
  except Exception as ex:
    print(f"[bold red] [!] ERROR CRÍTICO: {str(ex)} [/bold red]")
    return None
  finally:
    if 'auxVideo' in locals() and isinstance(auxVideo, VideoFileClip):
      auxVideo.close()


#——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
 # function | extractTitleFromMedia | extrate el titulo del video a traves de las URL ->
def extractTitleFromMedia(inputVideoURL, downloadPath="."):
  videoTitleCommand = [
    "yt-dlp",
    "--print", "filename",
    "-o", os.path.join(str(downloadPath), "%(title)s.%(ext)s"),
    inputVideoURL
  ]

  try:
    outputFilename = subprocess.check_output(
      videoTitleCommand,
      shell=False,
      stderr=subprocess.PIPE,
      text=True
    ).strip()
    return outputFilename
  
  except subprocess.CalledProcessError as ex:
    print(f"[bold red] [!] ERROR: {ex.stderr if ex.stderr else str(ex)} [/bold red]")
    return None
  
  except Exception as ex:
    print(f"[bold red] [!] ERROR: {str(ex)} [/bold red]")
    return None


 # import libraries ->
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from libraries.imports import *
from model.helpModel import *


#——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
 # function | downloadVideoFromURL | descargar un video a traves de la URL del video ->
def downloadVideoFromURL(inputOutputFolder, inputVideoURL):
  downloadPath = inputOutputFolder
  try:
    videoCommand = [
      "yt-dlp",
      "-f", "best[height<=720]/best",
      "-o", os.path.join(str(downloadPath), "%(title)s.%(ext)s"),
      inputVideoURL,
    ]
    result = subprocess.run(
      videoCommand,
      shell=False,
      check=True,
      capture_output=True,
      text=True
    )
    
    actualFilesCommand = [
      "yt-dlp",
      "--print", "after_move:filepath",
      "-f", "best[height<=720]/best",
      "-o", os.path.join(str(downloadPath), "%(title)s.%(ext)s"),
      "--simulate",
      inputVideoURL
    ]
    
    try:
      actualPath = subprocess.check_output(actualFilesCommand, text=True).strip()
      if os.path.exists(actualPath):
        return actualPath
    except:
      pass
    
    import glob
    pattern = os.path.join(str(downloadPath), "*")
    files = glob.glob(pattern)
    if files:
      newest_file = max(files, key=os.path.getctime)
      return newest_file
    
    videoTitleCommand = [
      "yt-dlp",
      "--print", "filename",
      "-o", os.path.join(str(downloadPath), "%(title)s.%(ext)s"),
      inputVideoURL
    ]
    outputFilename = subprocess.check_output(videoTitleCommand, text=True).strip()
    outputPath = outputFilename
    
    if not os.path.exists(outputPath):
      print(f"[bold red] [!] ERROR CRITICO: Archivo no encontrado: {outputPath} [/bold red]")
      return None
    return outputPath
  except subprocess.CalledProcessError as ex:
    print(f"[bold red] [!] ERROR CRITICO: {str(ex)} [/bold red]")
    if ex.stderr:
      print(f"[bold red] Detalles del error: {ex.stderr} [/bold red]")
    return None
  except Exception as ex:
    print(f"[bold red] [!] ERROR CRITICO: {str(ex)} [/bold red]")
    return None


#——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
# function | downloadAudioFromVideo | descargar el audio de un video a traves de la URL ->
def downloadAudioFromVideo(inputOutputFolder, inputVideoURL):
  downloadPath = inputOutputFolder
  auxVideo = None
  
  try:
    downloadVideoPath = downloadVideoFromURL(inputOutputFolder, inputVideoURL)
    
    if not downloadVideoPath or not os.path.exists(downloadVideoPath):
      print(f"[bold red] [!] ERROR CRÍTICO: No se pudo descargar el video [/bold red]")
      return None
      
    print(f"[green] Video descargado: {downloadVideoPath} [/green]")
    
    try:
      auxVideo = VideoFileClip(downloadVideoPath)
      if auxVideo.audio is None:
        print(f"[bold red] [!] ERROR: El video no contiene audio [/bold red]")
        return None
    except Exception as e:
      print(f"[bold red] [!] ERROR al abrir el video con MoviePy: {str(e)} [/bold red]")
      return extractAudioWithFFmpeg(downloadVideoPath, downloadPath)
    
    base_audio = os.path.splitext(os.path.basename(downloadVideoPath))[0]
    downloadAudioPath, *_ = getUniqueFilename(downloadPath, base_audio, ".mp3")
    
    try:
      auxVideo.audio.write_audiofile(
        downloadAudioPath,
        codec='mp3',
        bitrate='192k',
        ffmpeg_params=['-ar', '44100'],
        logger=None,
        verbose=False
      )
      print(f"[green] Audio extraído exitosamente: {downloadAudioPath} [/green]")
      
    except Exception as e:
      print(f"[bold red] [!] ERROR en extracción de audio: {str(e)} [/bold red]")
      return extractAudioWithFFmpeg(downloadVideoPath, downloadPath)
    
    try:
      os.remove(downloadVideoPath)
      print(f"[green] Archivo temporal eliminado: {downloadVideoPath} [/green]")
    except:
      pass
      
    return downloadAudioPath
    
  except Exception as ex:
    print(f"[bold red] [!] ERROR CRÍTICO: {str(ex)} [/bold red]")
    return None
    
  finally:
    if auxVideo is not None:
      try:
        auxVideo.close()
      except:
        pass


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


#——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
 # function | extractAudioWithFFmpeg | extrae el audio con FFmepg ->
def extractAudioWithFFmpeg(videoPath, outputFolder):
  try:
    base_audio = os.path.splitext(os.path.basename(videoPath))[0]
    audioPath, *_ = getUniqueFilename(outputFolder, base_audio, ".mp3")
    
    ffmpeg_command = [
      "ffmpeg",
      "-i", videoPath,
      "-vn",
      "-acodec", "mp3",
      "-ab", "192k",
      "-ar", "44100",
      "-y",
      audioPath
    ]
    
    result = subprocess.run(
      ffmpeg_command,
      check=True,
      capture_output=True,
      text=True
    )
    
    if os.path.exists(audioPath):
      print(f"[green] Audio extraído con FFmpeg: {audioPath} [/green]")

      try:
        os.remove(videoPath)
      except:
        pass
      return audioPath
    else:
      print(f"[bold red] [!] ERROR: No se pudo crear el archivo de audio [/bold red]")
      return None
      
  except subprocess.CalledProcessError as ex:
    print(f"[bold red] [!] ERROR FFmpeg: {str(ex)} [/bold red]")
    if ex.stderr:
      print(f"[bold red] Detalles: {ex.stderr} [/bold red]")
    return None
  except Exception as ex:
    print(f"[bold red] [!] ERROR: {str(ex)} [/bold red]")
    return None


#——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
 # function | downloadAudioDirectly | descarga el audio directamente sin pasar por el video y la conversion ->
def downloadAudioDirectly(inputOutputFolder, inputVideoURL):
  downloadPath = inputOutputFolder
  
  try:
    titleCommand = [
      "yt-dlp",
      "--print", "title",
      inputVideoURL
    ]
    
    title = subprocess.check_output(titleCommand, text=True).strip()
    base_audio = title.replace("/", "_").replace("\\", "_")
    audioPath, *_ = getUniqueFilename(downloadPath, base_audio, ".mp3")
    
    audioCommand = [
      "yt-dlp",
      "-x",
      "--audio-format", "mp3",
      "--audio-quality", "192K",
      "-o", audioPath.replace(".mp3", ".%(ext)s"),
      inputVideoURL
    ]
    
    result = subprocess.run(
      audioCommand,
      check=True,
      capture_output=True,
      text=True
    )
    
    if os.path.exists(audioPath):
      print(f"[green] Audio descargado directamente: {audioPath} [/green]")
      return audioPath
    else:
      print(f"[bold red] [!] ERROR: No se pudo descargar el audio [/bold red]")
      return None
      
  except subprocess.CalledProcessError as ex:
    print(f"[bold red] [!] ERROR yt-dlp: {str(ex)} [/bold red]")
    return None
  except Exception as ex:
    print(f"[bold red] [!] ERROR: {str(ex)} [/bold red]")
    return None
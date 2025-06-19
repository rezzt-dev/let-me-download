 # import libraries ->
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from libraries.imports import *
from model.helpModel import *
from model.mediaModel import *


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
    if boolVideo:
      downloadVideoFromURL(subcontainerFolder, videoURL)
    if boolAudio:
      downloadAudioFromVideo(subcontainerFolder, videoURL)

    mediaName = extractTitleFromMedia(videoURL)
    if mediaName != None:
      downloadedMediaDone.append(videoURL)
    else:
      counter += 1
      mediaName = f"video-downloaded-{counter}"
      downloadedMediaDone.append(videoURL)
  return downloadedMediaDone
 # import libraries ->
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from libraries.imports import *
from model.helpModel import selectURLfiles, returnYesNoQuestion, loadingAnimation, waitKey
from controller.generalController import executeController


#——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
 # function | runMainWindow | ejecuta la ventana principal de la aplicacion ->
def runMainWindow():
  while True:
    os.system('cls' if os.name == 'nt' else 'clear')
    print("[bold purple] -| Let-Me-Download / Python Tool |- [/bold purple]")

    videoURLfile = selectURLfiles()
    print(f"  -> Ruta del fichero que contiene las URLs de los videos: {videoURLfile}")

    onlyVideo = str(input("   => Quieres descargar el video s/n (default: s): "))
    onlyAudio = str(input("   => Quieres descargar solo el audio s/n (default: n): "))

    boolOnlyVideo = returnYesNoQuestion(onlyVideo)
    boolOnlyAudio = returnYesNoQuestion(onlyAudio, True)

    if (boolOnlyVideo == False) and (boolOnlyAudio == False):
      print("[bold red] [!] ERROR CRITICO. Tienes que seleccionar al menos una opcion.[/bold red]")
      print("[bold yellow]  -> Pulsa una tecla para continuar...[/bold yellow]")
      waitKey()
      continue

    downloadedMediaList = []

    print("")
    stopEvent = threading.Event()
    animationThread = threading.Thread(target=loadingAnimation, args=(stopEvent,))
    animationThread.start()

    downloadedMediaList = executeController(videoURLfile, boolOnlyVideo, boolOnlyAudio)

    stopEvent.set()
    animationThread.join()

    for downloadedMedia in downloadedMediaList:
      print(f"[bold green] [+] ÉXITO! Descarga completada: {downloadedMedia} [/bold green]")

    closeProgramm = str(input("  -> Quieres descargar mas videos s/n (default: n): "))
    boolCloseProgramm = returnYesNoQuestion(closeProgramm, True)

    if boolCloseProgramm == True:
      continue
    else:
      print("\n[bold yellow] [+] Pulsa cualquier tecla para cerrar el programa...[/bold yellow]")
      waitKey()
      break
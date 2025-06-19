 # import libraries ->
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from libraries.imports import *


#——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
 # function | getDownloadFolderPath | obtiene la ruta de descargas del sistema ->
def getDownloadFolderPath ():
  homePath = Path.home()
  downloadsPath = homePath / "Downloads"
  descargasPath = homePath / "Descargas"

  returnedPath = None
  if downloadsPath.exists() and downloadsPath.is_dir():
    returnedPath = str(downloadsPath)
  elif descargasPath.exists() and descargasPath.is_dir():
    returnedPath = str(descargasPath)
  return returnedPath


#——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
 # function | waitKey | espera a que el usuario pulse cualquier tecla ->
def waitKey():
  fd = sys.stdin.fileno()
  old_settings = termios.tcgetattr(fd)
  try:
    tty.setraw(fd)
    ch = sys.stdin.read(1)
  finally:
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
  return ch


#——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
 # function | getUniqueFilename | obtiene el nombre del fichero para evitar sobreescribirlo ->
def getUniqueFilename (inputBasePath, inputBasename, inputExtension):
  counter = 0
  while True:
    if counter == 0:
      filename = f"{inputBasename}{inputExtension}"
    else:
      filename = f"{inputBasename}_{counter}{inputExtension}"
    fullPath = os.path.join(inputBasePath, filename)
    if not os.path.exists(fullPath):
      return fullPath, filename
    counter += 1


#——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
 # function | createContainerFolder | crea una carpeta para guardar los media-files dentro ->
def createContainerFolder():
  downloadPath = getDownloadFolderPath()
  containerFolder = Path(str(f"{downloadPath}/let-me-download"))

  if not containerFolder.exists():
    containerFolder.mkdir(exist_ok=True)

  return containerFolder


#——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
 # function | generateDatetimeString | genera un string con la fecha actual ->
def generateDatetimeString():
  nowDate = datetime.now()
  return nowDate.strftime('%d-%m-%Y_%H-%M')


#——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
 # function | loadingAnimation | ejecuta una animacion mientras se ejecuta una funcion ->
def loadingAnimation(stopEvent):
  icons = ["◸", "◹", "◿", "◺"]
  idx = 0
  console = Console()
  while not stopEvent.is_set():
    console.print(f"[bold blue]\r  [{icons[idx]}] Descargando los recursos del video... [/bold blue]", end="\r")
    idx = (idx + 1) % len(icons)
    time.sleep(0.2)
  console.print(" " * 70, end="\n\n")


#——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
 # function | selectURLfiles | selecciona el fichero que contiene las URLs ->
def selectURLfiles ():
  root = tk.Tk()
  root.withdraw()

  while True:
    filePath = filedialog.askopenfilename(
      title="Selecciona el archivo que contiene las URLs",
      filetypes=[("Archivos de texto", "*.txt")]
    )

    if not filePath:
      messagebox.showwarning("Advertencia", "Por favor, selecciona un archivo con extensión .txt")
      continue

    if filePath.lower().endswith('.txt'):
      return filePath
    messagebox.showwarning("Advertencia", "Por favor, selecciona un archivo con extensión .txt")


#——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
 # function | returnYesNoQuestion | devuelve true/false de una pregunta de s/n ->
def returnYesNoQuestion(inputStringValue: str, defaultFalse: bool = False) -> bool:
  questionValue = inputStringValue.strip().lower()

  if defaultFalse:
    return questionValue == "s"
  else:
    return questionValue != "n"
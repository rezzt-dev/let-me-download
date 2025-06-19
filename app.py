 # import libraries ->
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from libraries.imports import *
from view.generalWindow import runMainWindow


#——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
 # function | _runProgramm | function principal que ejecuta el programa ->
def _runProgramm():
  typer.run(runMainWindow)


#——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
 # code runner | codido para ejecutar la funcion en un entorno seguro ->
if __name__ == "__main__":
  typer.run(_runProgramm)
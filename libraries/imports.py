 # import libraries | librerias completas ->
import typer
import time
import termios
import tty
import subprocess
import threading
import tkinter as tk
import spotipy


#——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
 # import modules | modulos especificos de las librerias ->
from rich import print
from rich.console import Console

from pathlib import Path
from moviepy import VideoFileClip
from datetime import datetime

from tkinter import filedialog
from tkinter import messagebox

from spotipy.oauth2 import SpotifyClientCredentials
from pytube import Search, YouTube
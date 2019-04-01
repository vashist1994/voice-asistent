import speech_recognition as sr
from gtts import gTTS
import os
import sys
import re
# import pyttsx3
import webbrowser
import smtplib
import requests
import subprocess
from pyowm import OWM
import youtube_dl
import vlc
import urllib
from urllib.request import urlopen
from urllib.request import urlretrieve
import json
from bs4 import BeautifulSoup as soup
import wikipedia
import random
from time import strftime

r = sr.Recognizer()
with sr.Microphone() as source:
    print('Say something...')
    # r.pause_threshold = 1
    r.adjust_for_ambient_noise(source, duration=1)
    audio = r.listen(source)
    command=r.recognize_google(audio).lower()
    myobj = gTTS(text=str(command), lang='en', slow=False) 
    myobj.save("welcome.mp3") 
    os.system("mpg321 welcome.mp3")


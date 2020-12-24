#ti amo.
#{ }
import pyttsx3
import datetime
import speech_recognition as sr
import subprocess
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QAbstractButton, QApplication, QLabel, QMainWindow, QPushButton, QSizePolicy, QVBoxLayout, QWidget
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import pyjokes
import wikipedia
import threading
import webbrowser
import re
import json
import csv
from io import StringIO
import bs4
from bs4 import BeautifulSoup
import requests
import laurqrc

#voce
engine = pyttsx3.init()
engine.setProperty('rate', 125)
voices = engine.getProperty('voices')
voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_IT_ELSA_11.0"
engine.setProperty('voice', voice_id)

#definizione abilità
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def time():
    Time = datetime.datetime.now().strftime("%I:%M:%S")
    speak(Time)

def date():
    year = int(datetime.datetime.now().year)
    month = int(datetime.datetime.now().month)
    date = int(datetime.datetime.now().day)
    speak(date)
    speak(month)
    speak(year)

def wishme():
    hour = datetime.datetime.now().hour
    if hour >= 6 and hour<12:
        speak("buon giorno!")
    elif hour >= 12 and hour<18:
        speak("buon pomeriggio!")
    elif hour >= 18 and hour<24:
        speak("buona sera!")
    else:
        speak("buona notte!")
    speak("mi chiamo laura")
    speak("sono le")
    time()
    speak("oggi è il")
    date()
    speak("come posso aiutarti?")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("ascoltando...")
        r.pause_treshold = 1
        audio = r.listen(source)
        
    try:
        print("riconoscendo...")
        query = r.recognize_google(audio, language='it')
        print(query)

    except Exception as e:
        print(e)
        speak("ripeti per favore...")

        return "none"

    def note(text):
        date = datetime.datetime.now()
        file_name = str(date).replace(":", "-") + "-note.txt"
        with open(file_name, "w") as f:
            f.write(text)

        subprocess.Popen(["notepad.exe", file_name])

    def joke():
        speak(pyjokes.get_joke(language='it', category='neutral'))

    def compliments():
        speak("grazie mille")

    #parole chiave
    if "Ciao" in query:
            speak("ciao come stai?")
        
    if "chiami" in query:
            speak("mi chiamo laura")
        
    if "ora" in query:
            speak("sono le")
            time()

    if "giorno" in query:
            speak("oggi è il")
            date()

    if "presentati" in query:
            wishme()

    if "barzelletta" in query:
            joke()
            
    def get_audio():
        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio = r.listen(source)
            said = ""

            try:
                said = r.recognize_google(audio, language='it')
                print(said)
            except Exception as e:
                print(e)
        return said
    text = get_audio()

    def ricerca():
        wikipedia.set_lang("it")
        speak("cosa vuoi che cerchi?")
        polpetta = get_audio()
        data = wikipedia.summary(polpetta, 2)  
        speak(data) 

    def internet():
        speak("cosa vuoi che cerchi?")
        text = get_audio()
        url = 'https://www.duckduckgo.com/?q=' + text
        webbrowser.get().open(url)
        #speak("ecco cosa ho trovato per" + text)

    def tprice():
        speak("che ticker vuoi che cerchi?")
        ticker = get_audio()
        r = requests.get('https://finance.yahoo.com/quote/' + ticker + '/')
        soup = bs4.BeautifulSoup(r.text,"xml")
        price = soup.find_all('div',{'class':'My(6px) Pos(r) smartphone_Mt(6px)'})[0].find('span').text
        return price
    while True:
        print('the current price is' + str(tprice()))
        
    if "nota" in query:
        speak("cosa vuoi che scriva?")
        write_down = get_audio()
        note(write_down)
        speak("l'ho annotato")

    if "Wikipedia" in query:
        ricerca()

    if "internet" in query:
        internet()
  
    if "brava" in query:
        compliments()

    if "prezzo" in query:
        tprice()

    return query

    #you wanna see some real speed bitches
    t=threading.Thread(target=takeCommand,args=())
    t.start()
    t1=threading.Thread(target=speak(get_audio()),args=())
    t2=threading.Thread(target=speak(internet()),args=())
    #t3=threading.Thread(target=speak(ricerca()),args=())
    #t4=threading.Thread(target=speak(note(text)),args=())



#user interface
class MoviePlayer(QWidget): 
    def __init__(self, parent=None): 
        QWidget.__init__(self, parent)
        self.setGeometry(200, 200, 400, 400)
        self.setWindowTitle("Laura AI")
        self.setWindowIcon(QtGui.QIcon('Queen_Cortana.png'))
        self.setStyleSheet("background-color: rgb(0, 0, 0);")
        
        self.movie_screen = QLabel()

        btn_start = QPushButton()
        '''btn_start.setStyleSheet("border :10px solid ;"
                     "border-top-color :blue; "
                     "border-left-color :blue;"
                     "border-right-color :blue;"
                     "border-bottom-color :blue")'''
        btn_start.setIcon(QIcon("microphone2.png")) 
        size = QSize(100, 100) 
        btn_start.setIconSize(size)
        btn_start.clicked.connect(takeCommand)
        
        main_layout = QVBoxLayout() 
        main_layout.addWidget(self.movie_screen)
        main_layout.addWidget(btn_start) 
        self.setLayout(main_layout)
                
        self.movie = QMovie("image6.gif", QByteArray(), self) 
        self.movie.setCacheMode(QMovie.CacheAll) 
        self.movie.setSpeed(100) 
        self.movie_screen.setMovie(self.movie) 
        self.movie.start()

app = QApplication(sys.argv) 
player = MoviePlayer() 
player.show() 
sys.exit(app.exec_())

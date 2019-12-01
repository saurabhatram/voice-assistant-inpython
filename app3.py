import pyttsx3  # pip install pyttsx3
import speech_recognition as sr  # pip install speechRecognition
import datetime
import wikipedia  # pip install wikipedia
import webbrowser
import os
import smtplib
import pyaudio
import sqlite3
from googlesearch import search

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def takeCommand():
    # It takes microphone input from the user and returns string output

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        # print(e)
        print("Say that again please...")
        return "None"
    return query


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")

    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")

    else:
        speak("Good Evening!")

    speak("I am SWAEYAAM Sir. Please tell me how may I help you")


def search_db(q):
    global abc
    conn = sqlite3.connect("websites.db")
    c = conn.cursor()
    c.execute("SELECT web_path FROM websites WHERE web_id = ?", (q,))
    rows = str(c.fetchall())

    if rows == "[]":
        print("Sorry try again")
    else:
        abc = rows[3:-4]
        print(rows[3:-4])
    conn.close()
    return abc


def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('jarvissdl@gmail.com', 'jarvis@123')
    server.sendmail('jarvissdl@gmail.com', to, content)
    server.close()


if __name__ == "__main__":

    wishMe()

    while True:
        # if 1:

        query = takeCommand().lower()

        # Logic for executing tasks based on query
        # ----------------------------------------------------------------------website search
        if 'wikipedia' in query:  # tell something like wikipedia newton
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)
            speak(
                f"do you want more information about {query} then say yes ")  # if you want a wikipedia page to open say yes
            query_wiki = takeCommand()
            if 'yes' in query_wiki:
                webbrowser.open("https://en.wikipedia.org/wiki/" + ''.join(query))


        elif 'open website' in query:  # tell open website
            try:
                speak('which website do you want to search')  # tell it only website name not .com .co.in etc
                query2 = takeCommand().lower()
                webbrowser.open(search_db(query2))
            except Exception as e:
                print(e)
                speak("Sorry, I am not able to search this website")

        elif 'google' in query:  # tell google newton it will open 1st tab as well as give us results

            indx = query.lower().split().index('google')
            query = query.split()[indx + 1:]
            webbrowser.open("https://www.google.com/search?q=" + '+'.join(query))
            for j in search(str(query), tld="co.in", num=10, stop=1, pause=2):
                webbrowser.open(j)

        elif 'youtube' in query:  # tell youtube newton it will give search results on newton
            indx = query.lower().split().index('youtube')
            query = query.split()[indx + 1:]
            webbrowser.open("http://www.youtube.com/results?search_query=" + '+'.join(query))

        # ---------------------------------------------------------------------website search ends here

        # ----------------------------------------------------------------------sending email

        elif 'email to sumit' in query:
            try:
                speak("What should I say?")
                content = takeCommand()
                to = "saurabhatram99@gmail.com"
                sendEmail(to, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("I am not able to send this email a problem occured")

        # ---------------------------------------------------------------------email ends

        # ---------------------------------------------------------------------know time
        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            print(f"Sir, the time is {strTime}")
            speak(f"Sir, the time is {strTime}")
        # ----------------------------------------------------------------------time ends

        # ---------------------------------------------------------------------Play music
        elif 'play music' in query:
            music_dir = 'F:\\music'
            songs = os.listdir(music_dir)
            print("Playing Song!!!")
            print(songs)
            os.startfile(os.path.join(music_dir, songs[0]))
        # ---------------------------------------------------------------------Play music ends

        # ---------------------------------------------------------------------open code
        elif 'open code' in query:
            codePath = "C:\\Program Files (x86)\\Arduino\\arduino.exe"
            print("Opening code")
            os.startfile(codePath)
        # ---------------------------------------------------------------------open code ends

        # ---------------------------------------------------------------------shutdown
        elif 'turn off'in query:
            print("Shutting down sir")
            speak("Shutting down sir")
            break
        # ---------------------------------------------------------------------shut down ends-

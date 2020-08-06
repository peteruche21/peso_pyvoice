import requests
import os
import subprocess
import json
import smtplib
import ssl
import webbrowser
import time

from datetime import datetime
from random import randint
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import wikipedia
import pyautogui
import psutil
import pyttsx3 as tts
import speech_recognition as stt
from bs4 import BeautifulSoup as beasoup


class Emailing(object):

    SMTP_CONFIG = {
        'server': 'smtp.aol.com',
        'username': 'pmanager25@aol.com',
        'password': 'nbfkgtcfdytlsief',
        'port': 465
    }
    CONTEXT = ssl.create_default_context()

    def __init__(self):
        smtp_config = self.SMTP_CONFIG
        context = self.CONTEXT

        self.connection = smtplib.SMTP_SSL(smtp_config['server'],
                                           smtp_config['port'],
                                           context=context)
        self.connection.login(smtp_config['username'], smtp_config['password'])

    def send(self, reciever, message):
        sender = self.SMTP_CONFIG['username']
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['T0'] = reciever
        msg['Subject'] = 'reset'

        body = f"<h1>{message}</h1>"
        msg.attach(MIMEText(body, 'html'))
        self.connection.sendmail(sender, reciever, msg.as_string())
        speak('email sent, \nplease note: it may be in spam folder')


def speak(query: str):
    engine = tts.init()
    engine.setProperty('rate', 137)
    engine.say(query)
    engine.runAndWait()


def current_time():
    current_time = time.strftime('%I:%M %p')
    speak(f'the time is {current_time}')


def current_date():
    current_date = datetime.now()
    current_date = '{:%B %d, %Y}'.format(current_date)
    speak(f"today's date is {current_date}")


def current_weather(query: str):
    api_key = '21c6aeaa3df35ea4e399e6e5470dd077'
    url = f"https://api.openweathermap.org/data/2.5/weather?q={query}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = json.loads(response.text)
        print(data)
        temperature = data["main"]["temp"]
        clouds = data["clouds"]["all"]
        humidity = data["main"]["humidity"]
        weather = data["weather"][0]["description"]
    else:
        weather_details = "sorry, i can not retrieve the weather forecast of your location at this time, sorry"
    speak(weather_details)


def wikipedia_search(query: str):
    wikipedia.set_lang('en')
    result = wikipedia.search(query, results=3)
    one_in_result = wikipedia.summary(result[randint(0, len(result) - 1)])
    speak(one_in_result)


def google_search(query: str):
    print(browser._browsers)
    chrome_path = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
    speak('opening default browser ...')
    webbrowser.register('chrome', None, webbrowser.Chrome(chrome_path))
    webbrowser.get('chrome').open_new_tab(f"https://www.google.com?&q={query}")


def location_now():
    response = requests.get("https://ipinfo.io")
    if response.status_code == 200:
        data = json.loads(response.text)
        location = data["city"] + ' in ' + data["region"] + ', ' + data[
            "country"]
        print(data)
    else:
        location = 'i could not retrieve your location at this time, sorry'
    speak(location)


def tell_a_joke():
    response = requests.get("http://api.icndb.com/jokes/random")
    if response.status_code == 200:
        data = json.loads(response.text)
        joke = data["value"]["joke"]
    else:
        joke = 'i could not retrieve a joke at this time, sorry'
    speak(joke)


def tell_a_quote():
    response = requests.get('https://api.quotable.io/random')
    if response.status_code == 200:
        data = json.loads(response.text)
        quote = f'{data["content"]} ({data["author"]})'
    else:
        quote = 'I could not retrieve a quote at this time, sorry.'
    speak(quote)


def launch_chrome():
    chrome_path = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
    webbrowser.register('chrome', None, webbrowser.Chrome(chrome_path))
    speak('opening chrome browser ...')
    webbrowser.get('chrome')


def launch_firefox():
    firefox_path = "C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe"
    webbrowser.register('firefox', None, webbrowser.Mozilla(firefox_path))
    speak('opening firefox browser ...')
    webbrowser.get('firefox')


def launch_vscode():
    speak("opening visual studio insider edition ...")
    subprocess.Popen(
        "C:\\Users\\USER\\AppData\\Local\\Programs\\Microsoft VS Code Insiders\\Code - Insiders.exe"
    )


def launch_pycharm():
    speak('opening pycharm IDE ...')
    subprocess.Popen(
        "C:\\Program Files\\JetBrains\\PyCharm 2019.2\\bin\\pycharm64.exe")


def send_email():
    speak('please enter reciepient ...')
    reciever = input('>>> ')
    speak('enter your message ...')
    message = input('>>> ')
    Emailing().send(reciever, message)


def play_music():
    music_dir = 'C:\\Users\\USER\\Music'
    musics = os.listdir(music_dir)
    speak('playing you a music!')
    os.startfile(os.path.join(music_dir, musics[randint(0, len(musics) - 1)]))


def screenshot():
    screenshot = pyautogui.screenshot('images/' +
                                      f"{int(time.time() * 1000)}.png")


def system_properties():
    cpu_usage = str(psutil.cpu_percent())
    battery_percentage = psutil.sensors_battery()
    battery_percent = battery_percentage.percent
    battery_time = round(battery_percentage.secsleft / 3600, 2)
    charging = battery_percentage.power_plugged
    core = psutil.cpu_count()
    memmory = psutil.virtual_memory()
    memory = round(memmory.total / 1000000000)
    free_mem = round(memmory.free / 1000000000, 1)
    used_mem = round(memmory.used / 1000000000, 1)
    mem_percent = memmory.percent
    if charging:
        speak(f"""
        your computer is currently charging. i can not get your uptime at this time.
        your CPU is running on {core} cores.
        total memory installed is {memory} gigabyte, {mem_percent}% of this estimated at {used_mem} gigabyte is occupied,
        while {100 - int(mem_percent)}% estimated at {free_mem} gigabyte is free {'consider closing some applications' if used_mem > 80 else '.'} 
        """)
    else:
        speak(f"""
        your computer uptime is estimated at {str(battery_time).replace('.', 'hours ')}minutes, 
        which stands at {battery_percent}% of available power.
        your CPU is running on {core} cores.
        total memory installed is {memory}GB, {mem_percent}% of this estimated at {used_mem}GB is occupied,
        while {100 - int(mem_percent)}% estimated at {free_mem} is free {'consider closing some applications' if used_mem > 80 else '.'} 
        """)


def recieve_voice_input() -> str:
    sr = stt.Recognizer()
    with stt.Microphone() as source:
        sr.pause_threshold = 1
        audio = sr.listen(source, timeout=5)
    try:
        text = sr.recognize_google(audio, language='en-US')
    except Exception as e:
        return 0

    return text.casefold()


def welcome():
    speak('''
    welcome Peso, to your python voice assistant.
    what do you want to do?
    ''')
    command = recieve_voice_input()
    if command:
        return command
    else:
        speak('please say something')


def main():
    command = welcome()
    while True:
        if 'time' in command:
            current_time()
        elif 'date' in command:
            current_date()
        elif ('quit' or 'thank you') in command:
            speak('ok!, if you need me again, just run this py file')
            quit()
        elif ('weather' or 'rain') in command:
            speak('Please enter your city name to get weather forecast')
            city = input('enter your city:\n>>> ')
            current_weather(city)
        elif 'location' in command:
            location_now()
        elif 'quote' in command:
            tell_a_quote()
        elif 'logout' in command:
            os.system("shutdown -l")
        elif 'restart' in command:
            os.system("shutdown /r /t 1")
        elif 'shutdown' in command:
            os.system("shutdown /s /t 1")
        elif ('search google' or 'search' or 'browse') in command:
            pass
        elif ('wikipedia' or 'wiki') in command:
            pass

        elif 'joke' in command:
            pass
        elif ('launch chrome' or 'open chrome' or 'open browser' or 'browser'
              or 'chrome') in command:
            pass
        elif ('launch firefox' or 'open firefox' or 'firefox') in command:
            pass
        elif ('pycharm' or 'pie charm') in command:
            pass
        elif ('music' or 'play music' or 'song') in command:
            pass
        elif 'screenshot' in command:
            pass
        elif ('email' or 'mail') in command:
            pass
        elif ('vs code' or 'code editor' or 'VScode') in command:
            pass
        else:
            speak("sorry i didn't get that try to rephrase your sentence to\
                 include the keyword of the action you want me to perform")
        command = recieve_voice_input()

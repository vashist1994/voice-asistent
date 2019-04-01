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



# Dictionary to launch the appliations
application = {
    'chrome':'google-chrome',
    'calendar': 'gnome-calendar',
    # 'calculator': '',
    # 'vs code': 'code.'
}
def sofiaResponse(audio):
    "speaks audio passed as argument"
    print(audio)
    # engine = pyttsx3.init()
    # engine.say('Good morning.')
    # splitedaudio = audio.splitlines()
    # os.system('espeak -s 120 -v en+m6 -p 15   "{}"'.format(audio))
    myobj = gTTS(text=str(audio), lang='en', slow=False) 
    myobj.save("welcome.mp3") 
    os.system("mpg321 welcome.mp3")

    # print("------: ",splitedaudio)
    # for line in splitedaudio:
    #     print("====>: ", line)
    #     # print("@@@@@@>:",type(line))
    #     os.system("espeak -v female3 " + str(line))
    #     # os.system("espeak " + str(line))

def myCommand():
    "listens for commands"
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Say something...')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio).lower()
        print('You said: ' + command + '\n')
    #loop back to continue to listen for commands if unrecognizable speech is received
    except sr.UnknownValueError:
        print('....')
        command = myCommand();
    return command

def assistant(command):
    "if statements for executing commands"
    #open subreddit Reddit
    if 'open reddit' in command:
        reg_ex = re.search('open reddit (.*)', command)
        url = 'https://www.reddit.com/'
        if reg_ex:
            subreddit = reg_ex.group(1)
            url = url + 'r/' + subreddit
        webbrowser.open(url)
        sofiaResponse('The Reddit content has been opened for you Sir.')
    elif 'shutdown' in command:
        sofiaResponse('Bye bye Sir. Have a nice day')
        subprocess.run(["shutdown", '-h', 'now'])
        sys.exit()
        
    #open website
    elif 'open' in command:
        reg_ex = re.search('open (.+)', command)
        if reg_ex:
            domain = reg_ex.group(1)
            print(domain)
            url = 'https://www.' + domain
            webbrowser.open(url)
            sofiaResponse('The website you have requested has been opened for you Sir.')
        else:
            pass
    
    # google search
    if "search" in command:
        command = command.split(" ")
        text = command[1]
        f_text = "https://www.google.com/search?q="+text
        # domain = reg_ex.group(1)
        # print(domain)
        url = f_text
        sofiaResponse("Hold on sir, I will show  you the" + text + " search result.")
        webbrowser.open(url)
        
        
        # os.system("google-browser https://www.google.nl/maps/place/" + location + "/&amp;")
    
    #greetings
    elif 'hello' in command:
        day_time = int(strftime('%H'))
        if day_time < 12:
            sofiaResponse('Hello Sir. Good morning')
        elif 12 <= day_time < 18:
            sofiaResponse('Hello Sir. Good afternoon')
        else:
            sofiaResponse('Hello Sir. Good evening')

    elif 'help me' in command:
        sofiaResponse("""
        You can use these commands and I'll help you out:
        1. Open reddit subreddit : Opens the subreddit in default browser.
        2. Open xyz.com : replace xyz with any website name
        3. Send email/email : Follow up questions such as recipient name, content will be asked in order.
        4. Current weather in {cityname} : Tells you the current condition and temperture
        5. Hello
        6. play me a video : Plays song in your VLC media player
        7. change wallpaper : Change desktop wallpaper
        8. news for today : reads top news of today
        9. time : Current system time
        10. top stories from google news (RSS feeds)
        11. tell me about xyz : tells you about xyz
        12. Search xyz : search xyz on your default browser
        13. shutdown : To shutdown your system
        14. Reboot : To Reboot your system
        """)
    #joke
    elif 'joke' in command:
        res = requests.get(
                'https://icanhazdadjoke.com/',
                headers={"Accept":"application/json"})
        if res.status_code == requests.codes.ok:
            sofiaResponse(str(res.json()['joke']))
        else:
            sofiaResponse('oops!I ran out of jokes')
    #top stories from google news
    elif 'news for today' in command:
        try:
            news_url="https://news.google.com/news/rss"
            Client=urlopen(news_url)
            xml_page=Client.read()
            Client.close()
            soup_page=soup(xml_page,"xml")
            news_list=soup_page.findAll("item")
            for news in news_list[:15]:
                sofiaResponse(news.title.text.encode('utf-8'))
        except Exception as e:
            print(e)

    #current weather
    elif 'current weather' in command:
        reg_ex = re.search('current weather in (.*)', command)
        if reg_ex:
            city = reg_ex.group(1)
            owm = OWM(API_key='ab0d5e80e8dafb2cb81fa9e82431c1fa')
            obs = owm.weather_at_place(city)
            w = obs.get_weather()
            k = w.get_status()
            x = w.get_temperature(unit='celsius')
            sofiaResponse('Current weather in %s is %s. The maximum temperature is %0.2f and the minimum temperature is %0.2f degree celcius' % (city, k, x['temp_max'], x['temp_min']))
    #time
    elif 'time' in command:
        import datetime
        now = datetime.datetime.now()
        sofiaResponse('Current time is %d hours %d minutes' % (now.hour, now.minute))
    
    elif 'email' in command:
        sofiaResponse('Who is the recipient?')
        recipient = myCommand()
        if 'rajat' in recipient:
            sofiaResponse('What should I say to him?')
            content = myCommand()
            mail = smtplib.SMTP('smtp.gmail.com', 587)
            mail.ehlo()
            mail.starttls()
            mail.login('your_email_address', 'your_password')
            mail.sendmail('sender_email', 'receiver_email', content)
            mail.close()
            sofiaResponse('Email has been sent successfuly. You can check your inbox.')
        else:
            sofiaResponse('I don\'t know what you mean!')
    #launch any application
    elif 'launch' in command:
        reg_ex = re.search('launch (.*)', command)
        # print(reg_ex)
        if reg_ex:
            appname = reg_ex.group(1)
            if appname in application.keys():
                # appname1 = appname
                print(appname)
                # subprocess.Popen(["xdg-open",   "google-chrome"], stdout=subprocess.PIPE)
                subprocess.run(application[appname], shell=True, stdout=subprocess.PIPE)
                sofiaResponse('I have launched the'+appname+'application')
            else:
                sofiaResponse("Sorry sir can't launch the"+appname+"application")


    
    #Restart the System
    elif 'reboot' in command:
        reg_ex = re.search('reboot (.*)', command)
        subprocess.run(["reboot"])

    #Shut Down the System

       

    #play youtube song
    elif 'play me a song' in command:
        path = '/home/vashist/Downloads/videos/'
        folder = path
        print("directories list>>>>:",os.listdir(folder))
        for the_file in os.listdir(folder):
            print("the_file: ", the_file)
            file_path = os.path.join(folder, the_file)
            print("file path: ", file_path)
            try:
                print("os.path.isfile(file_path)", os.path.isfile(file_path))
                if os.path.isfile(file_path):
                    print("os.unlink(file_path)", os.unlink(file_path))
                    os.unlink(file_path)
            except Exception as e:
                print(e)
        sofiaResponse('What song shall I play Sir?')
        mysong = myCommand()
        if mysong:
            flag = 0
            url = "https://www.youtube.com/results?search_query=" + mysong.replace(' ', '+')
            response = urlopen(url)
            html = response.read()
            soup1 = soup(html,"lxml")
            url_list = []
            for vid in soup1.findAll(attrs={'class':'yt-uix-tile-link'}):
                if ('https://www.youtube.com' + vid['href']).startswith("https://www.youtube.com/watch?v="):
                    flag = 1
                    final_url = 'https://www.youtube.com' + vid['href']
                    url_list.append(final_url)
                    url = url_list[0]
                    ydl_opts = {}
                    os.chdir(path)
                    print("os.chdir(path)",os.chdir(path))
                    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([url])
                        print("path: ", path)
                        vlc.play(path)
                        # media.play()
            if flag == 0:
                sofiaResponse('I have not found anything in Youtube ')
    #change wallpaper
    elif 'change wallpaper' in command:
        folder = '/Users/nageshsinghchauhan/Documents/wallpaper/'
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)
        api_key = 'fd66364c0ad9e0f8aabe54ec3cfbed0a947f3f4014ce3b841bf2ff6e20948795'
        url = 'https://api.unsplash.com/photos/random?client_id=' + api_key #pic from unspalsh.com
        f = urlopen(url)
        json_string = f.read()
        f.close()
        parsed_json = json.loads(json_string)
        photo = parsed_json['urls']['full']
        urlretrieve(photo, "/home/vashist/wallpaper/a") # Location where we download the image to.
        subprocess.call(["killall Dock"], shell=True)
        sofiaResponse('wallpaper changed successfully')

    #askme anything
    elif 'tell me about' in command:
        reg_ex = re.search('tell me about (.*)', command)
        try:
            if reg_ex:
                topic = reg_ex.group(1)
                ny = wikipedia.page(topic)
                sofiaResponse(ny.content[:500].encode('utf-8'))
        except Exception as e:
                print(e)
                sofiaResponse(e)    
sofiaResponse('Hi User, I am Jarvis and I am your personal voice assistant, Please give a command or say "help me" and I will tell you what all I can do for you.')  
                 
#loop to continue executing multiple commands
while True:
    assistant(myCommand())
import speech_recognition as sr # recognise speech input
import playsound # to play an audio file
from gtts import gTTS # google text to speech
import random
from time import ctime # get time details
import yfinance as yf # fetch financial data
import webbrowser # open a webbrowser
import time
import os # to remove created audio files

class person:
    name = ''
    def setName(self, name):
        self.name = name

def there_exists(terms):
    for term in terms:
        if term in voice_data:
            return True

r = sr.Recognizer() # intialize a recognizer

# listen for audio and convert it to text (strings):
def record_audio(ask = False):
    with sr.Microphone() as source: #choose microphone as source of input
        if ask:
            nala_speak(ask)

        audio = r.listen(source) # listen for the audio via source
        voice_data = ''
        try:
          voice_data = r.recognize_google(audio) # convert audio to text
        except sr.UnknownValueError: # error: recognizer does not understand input
          nala_speak('Sorry, I did not get that')
        except sr.RequestError: # error: recognizer is not connected
          nala_speak('Sorry, my central processing speech service is down')
        print(voice_data.lower()) # print what the user said
        return voice_data.lower()

# get string and create an audio file to be played
def nala_speak(audio_string):
    tts = gTTS(text=audio_string, lang='en') # text to speech (voice)
    r = random.randint(1, 20000000)
    audio_file = 'audio-' + str(r) + '.mp3'
    tts.save(audio_file) # save as mp3
    playsound.playsound(audio_file) # play the audio file
    print(audio_string) # print what nala said
    os.remove(audio_file) # remove audio file

# have nala respond to user
def respond(voice_data):
    # 1: greeting
    if there_exists(['hey', 'hi', 'hello', "what's up", 'yo']):
        greetings = [f"hey, how can I help you {person.name}?", f"hey, what's up? {person.name}", f"I'm listening, {person.name}", f"how can I help you {person.name}?", f"hello, {person.name}"]
        greet = greetings[random.randint(0, len(greetings) - 1)]
        nala_speak(greet)
    
    # 2: name
    if there_exists(["what is your name", "what's your name", "tell me your name"]):
        if person.name:
            nala_speak("my name is Nala")
        else:
            nala_speak("my name is Nala. what's your name?")

    if there_exists(['my name is']):
        person_name = voice_data.split("is")[-1].strip()
        nala_speak(f"Ok, I will remember that {person_name}")
        person.setName(person_name) # save person name
    
    # 3. polite
    if there_exists(["how are you", "how are you doing"]):
        nala_speak(f"I'm very well, thanks for asking {person.name}")
    
    # 4. time
    if there_exists(["what time is it", "what's the time", "tell me the time", "Nala what time is it", "time check"]):
        time = ctime().split(" ")[3].split(":")[0:2]
        if time[0] == "00":
            hours = '12'
        else:
            hours = time[0]
        minutes = time[1]
        time = f'{hours} {minutes}'
        nala_speak(time)
    
    # 5. search google
    if there_exists(["search for"]) and "youtube" not in voice_data:
        search_term = voice_data.split("for")[-1]
        url = f"https://google.com/search?q={search_term}"
        webbrowser.get().open(url)
        nala_speak(f"Ok, here's what I found for {search_term} on google")
    
    # 6. search youtube
    if there_exists(["youtube"]):
        search_term = voice_data.split("for")[-1]
        url = f"https://youtube.com/results?search_query={search_term}"
        webbrowser.get().open(url)
        nala_speak(f"Ok, here's what I found for {search_term} on youtube")
    
    # 7. stocks
    if there_exists(["price of"]):
        search_term = voice_data.lower().split(" of ")[-1].strip() #strip removes whitespace after/before a term in string
        stocks = {
            "apple":"AAPL",
            "microsoft":"MSFT",
            "facebook":"FB",
            "tesla":"TSLA",
            "bitcoin":"BTC-USD",
            "google":"GOOGL",
            "jpmorgan":"JPM",
            "hyatt":"H",
            "sony":"SNE",
            "bankofamerica":"BAC",
            "skyworks":"SWKS",
            "cdw":"CDW",
            "amazon":"AMZN",
            "macys":"M",
            "gap":"GPS",
            "dowjones":"DJI",
            "nasdaq":"IXIC",
            "starbucks":"SBUX",
            "disney":"DIS",
            "visa":"V",
            "paypal":"PYPL"
        }
        try:
            stock = stocks[search_term]
            stock = yf.Ticker(stock)
            
            stock_daily_data = stock.history(period="1d")
            stock_price = stock_daily_data['Close'].iat[0]
            stock_list = str(stock_price).split('.')
            stock_dollars = stock_list[0]
            if stock_list[1][0] == '0':
                stock_cents = stock_list[1][1] # if the cents leads with a zero, axe it and only give a single integer for cents
            else:
                stock_cents = stock_list[1]

            nala_speak(f'Ok {person.name}, the price of {search_term} is listed as closing today at: {stock_dollars} dollars and {stock_cents} cents')
        except:
            nala_speak(f"Sorry {person.name}, something went wrong here. I encountered an error while trying to check the price of {search_term}")
    
    # 8. exit
    if there_exists(["exit", "quit", "goodbye", "shutdown", "Nala shutdown", "turn off", "Nala turn off", "power down", "Nala power down", "power off", "Nala power off"]):
        nala_speak("Powering down")
        exit() # exit program

    

time.sleep(1)

person = person()
nala_speak('How can I help you?')
while 1:
    voice_data = record_audio()
    respond(voice_data)
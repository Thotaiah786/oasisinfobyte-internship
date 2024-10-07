import speech_recognition as sr
import pyttsx3
import datetime
import requests

recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print(f"User said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I did not understand that.")
            return ""
        except sr.RequestError:
            speak("Sorry, my speech service is down.")
            return ""

def tell_time():
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M:%S")
    speak(f"The current time is {current_time}")

def tell_date():
    today = datetime.date.today()
    speak(f"Today's date is {today}")

def search_web(query):
    url = f"https://www.google.com/search?q={query}"
    speak(f"Here are the search results for {query}")
    requests.get(url)  

def main():
    speak("Hello, how can I assist you today?")
    while True:
        command = listen()
        if "hello" in command:
            speak("Hello! How can I help you?")
        elif "time" in command:
            tell_time()
        elif "date" in command:
            tell_date()
        elif "search" in command:
            speak("What do you want to search for?")
            query = listen()
            if query:
                search_web(query)
        elif "exit" in command:
            speak("Goodbye!")
            break

if __name__ == "__main__":
    main()      


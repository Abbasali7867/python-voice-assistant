import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import pywhatkit
import requests
import os

# Initialize text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def take_command():
    """Capture audio input and convert to text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            print("Recognizing...")
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
        except sr.UnknownValueError:
            print("Sorry, I could not understand that. Please try again.")
            return None
        except sr.RequestError:
            print("Unable to connect to the speech recognition service.")
            return None
        return command.lower()

def tell_time():
    """Tell the current time."""
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M:%S")
    speak(f"The current time is {current_time}")

def search_wikipedia(query):
    """Search for a topic on Wikipedia."""
    try:
        result = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia:")
        speak(result)
    except wikipedia.exceptions.DisambiguationError as e:
        speak("The query has multiple results. Please be more specific.")
    except wikipedia.exceptions.PageError:
        speak("The page does not exist.")
    except Exception as e:
        speak("An error occurred while searching Wikipedia.")

def play_song(song_name):
    """Play a song on YouTube."""
    try:
        pywhatkit.playonyt(song_name)
        speak(f"Playing {song_name} on YouTube.")
    except Exception as e:
        speak("I encountered an error while trying to play the song.")

def get_weather(city):
    """Fetch weather information using OpenWeatherMap API."""
    api_key = "YOUR_API_KEY"  # Replace with your OpenWeatherMap API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url).json()
        if response["cod"] == 200:
            temp = response["main"]["temp"]
            weather = response["weather"][0]["description"]
            speak(f"The temperature in {city} is {temp}°C with {weather}.")
        else:
            speak("City not found. Please try again.")
    except Exception as e:
        speak("I encountered an error while fetching the weather details.")

def system_commands(command):
    """Handle basic system commands."""
    if "open notepad" in command:
        os.system("notepad")
    elif "shutdown" in command:
        speak("Shutting down the system.")
        os.system("shutdown /s /t 1")
    elif "restart" in command:
        speak("Restarting the system.")
        os.system("shutdown /r /t 1")
    elif "open youtube" in command:
        speak("Opening YouTube")
        os.system("start https://www.youtube.com")
    elif "search google" in command:
        query = command.replace("search google", "").strip()
        pywhatkit.search(query)
        speak(f"Searching for {query} on Google.")
    elif "open whatsapp" in command:
        speak("Opening WhatsApp")
        os.system("start whatsapp://")
    elif "open capcut" in command:
        speak("Opening CapCut")
        os.system("start CapCut")  # Ensure CapCut is installed and the path is correct
    elif "open obs studio" in command:
        speak("Opening OBS Studio")
        os.system("start obs64.exe")# Ensure OBS Studio is installed and the path is correct
    elif "open Notion" in command:
        speak("Opening OBS Studio")
        os.system("start Notion")
    else:
      speak("Sorry, I can't handle that command yet.")

def main():
    """Main function to run the assistant."""
    speak("Hello! I am Jarvis, your personal assistant. How can I assist you today?")
    while True:
        command = take_command()
        if not command:
            continue

        # Basic functionalities
        if "time" in command:
            tell_time()
        elif "play" in command:
            play_song(command.replace("play", "").strip())
        elif "search" in command:
            search_wikipedia(command.replace("search", "").strip())
        elif "weather" in command:
            get_weather(command.replace("weather in", "").strip())
        elif "exit" in command or "stop" in command:
            speak("Goodbye! Have a great day!")
            break
        else:
            system_commands(command)

# Run the assistant
if __name__ == "__main__":
    main()

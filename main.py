import speech_recognition as sr
import webbrowser
import pyttsx3
import urllib.parse
import requests
import os

# Initialize the recognizer and the text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = os.getenv("NEWS_API_KEY")  # Use environment variable for API key

# Function to speak out text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to process the command
def processCommand(command):
    # Example of opening web pages
    if "open google" in command.lower():
        webbrowser.open("https://www.google.com")
        speak("Opening Google")
    elif "open youtube" in command.lower():
        webbrowser.open("https://www.youtube.com")
        speak("Opening YouTube")
    elif "open linkedin" in command.lower():
        webbrowser.open("https://www.linkedin.com")
        speak("Opening LinkedIn")
    # Adding YouTube music search functionality
    elif "play music" in command.lower() or "play song" in command.lower():
        playYouTubeMusic(command)
    # For news headlines
    elif "news" in command.lower() or "read news" in command.lower():
        fetchNews()
    # Exit command
    elif "exit" in command.lower() or "stop" in command.lower():
        speak("Goodbye!")
        exit()
    else:
        speak("I'm not sure how to help with that.")

def fetchNews():
    r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")
    if r.status_code == 200:
        data = r.json()
        articles = data.get('articles', [])
        if articles:
            for article in articles:
                speak(article['title'])
        else:
            speak("No news articles found.")
    else:
        speak("Sorry, I couldn't fetch the news at the moment.")

# Function to play music from YouTube
def playYouTubeMusic(command):
    # Extract song name from the command
    song_name = command.replace("play music", "").replace("play song", "").strip()
    
    # URL encode the song name for a YouTube search
    query_string = urllib.parse.urlencode({"search_query": song_name})
    youtube_url = f"https://www.youtube.com/results?{query_string}"

    # Automatically open the YouTube search in the browser
    webbrowser.open(youtube_url)
    speak(f"Searching YouTube for {song_name}")

if __name__ == "__main__":
    speak("Initializing Jarvis...")
    while True:
        print("Recognizing...")
        try:
            # Listen for the word "Jarvis"
            with sr.Microphone() as source:
                print("Listening...")
                recognizer.adjust_for_ambient_noise(source, duration=1)  # Adjust for noise in the background
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)  # Increased timeout
                word = recognizer.recognize_google(audio)
                print(f"Recognized word: {word}")  # Debugging line

                if word.lower() == "jarvis":
                    speak("Yes?")
                    # Now listen to the command
                    with sr.Microphone() as source:
                        print("Jarvis Active...")
                        recognizer.adjust_for_ambient_noise(source, duration=1)
                        audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)
                        command = recognizer.recognize_google(audio)
                        processCommand(command)

        except sr.UnknownValueError:
            speak("Sorry, I didn't understand that. Please speak clearly.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
        except Exception as e:
            print(f"Error: {e}")

import speech_recognition as sr
import webbrowser
import pyttsx3
import pyjokes
import musicLibrary

# Initialize recognizer, engine, microphone, and joke generator
recognizer = sr.Recognizer()
engine = pyttsx3.init()
mic = sr.Microphone()

# Set preferred voice (female)
for voice in engine.getProperty('voices'):
    if "zira" in voice.name.lower() or "hazel" in voice.name.lower() or "female" in voice.name.lower():
        print(f"Using voice: {voice.name}")
        engine.setProperty('voice', voice.id)
        break

def speak(text):
    engine.say(text)
    engine.runAndWait()

def processCommand(command):
    command = command.lower()
    print("Processing your command...")

    # Web Commands
    sites = {
        "google": "https://www.google.com",
        "youtube": "https://www.youtube.com",
        "linkedin": "https://www.linkedin.com",
        "facebook": "https://www.facebook.com",
        "instagram": "https://www.instagram.com"
    }
    for site in sites:
        if f"open {site}" in command:
            speak(f"Opening {site}")
            webbrowser.open(sites[site])
            return

    # Jokes
    if "joke" in command:
        speak(pyjokes.get_joke())
        return

    # Music
    if "play" in command:
        for word in ["please", "could you", "would you", "for me"]:
            command = command.replace(word, "")
        song = command.replace("play", "").replace("song", "").strip()

        if not song:
            speak("You said play, but didn't mention a song name. Please say it.")
            return

        link = musicLibrary.music.get(song.lower())
        if link:
            speak(f"Playing {song} from your saved list.")
            webbrowser.open(link)
        else:
            speak(f"I don't have {song} saved. Searching YouTube for you.")
            webbrowser.open(f"https://www.youtube.com/results?search_query={song}")
        return

    # Exit
    if "stop" in command or "quit" in command:
        speak("Goodbye.")
        exit()

    # Fallback
    print(f"You said: {command}")
    speak("I didn't understand that command.")

def listen():
    with mic as source:
        try:
            print("Listening...")
            audio_data = recognizer.listen(source, timeout=3, phrase_time_limit=3)
            query = recognizer.recognize_google(audio_data)
            print("You said:", query)
            return query.lower()
        except sr.WaitTimeoutError:
            print("Timeout. Speak again...")
        except sr.UnknownValueError:
            print("Didn't catch that. Speak clearly...")
        except Exception as e:
            print(f"Error: {e}")
    return ""

if __name__ == "__main__":
    with mic as source:
        print("Calibrating mic for ambient noise...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Calibration done. Say 'Jarvis' to activate.")

    while True:
        query = listen()
        if query == "jarvis":
            print("Jarvis Activated")
            speak("Hey buddy, how can I help you?")
            command = listen()
            if command:
                processCommand(command)
            else:
                speak("I didn't catch that.")
        elif "stop" in query or "quit" in query:
            speak("Goodbye.")
            break

print("-------------[Please wait for the loading to end]-------------")
print("[System]: loading Modules...")
print("  speech recognition")
import speech_recognition as sr
print("  pyttsx3 - text to speech")
import pyttsx3
print("  web browser and operating system modules")
import webbrowser
import os
print("  trigger words")
import trigger
import musicLibrary
print("  google generative ai")
import google.generativeai as genai
import time
import datetime
print("[System]: loading functions...")

# --- Setup ---
engine = pyttsx3.init()
recognizer = sr.Recognizer()
genai.configure(api_key="AIzaSyDwMn4Bla7uxsBmT7Z1G0ove74VnhILsU4")

model = genai.GenerativeModel("gemini-1.5-flash-8b")
chat = model.start_chat(history=[])
chat.send_message("Always answer in short. not over 50 words if not told to. update your memory to remember this point.")
chat.send_message("Your name is friday and you are an AI assistant used for my laptop. my name is Harshit Maurya 15 years old and born on 15 dec 2009")

engine.setProperty('rate', 150)

# --- Voice Output ---
print("  speak function")
def speak(query):
    try:
        engine = pyttsx3.init('sapi5')
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)  # Change index if needed
        engine.setProperty('rate', 150)
        engine.say(query)
        print("Friday:", query)
        engine.runAndWait()
        engine.stop()
    except Exception as e:
        print("[Speak Error]:", e)

# --- Gemini LLM Processing ---
print("  gemini request handling")
def ask_gemini(query):
    speak("Let me think...")
    try:
        response = chat.send_message(query)
        text = response.text
        speak(text)
    except Exception as e:
        speak("Sorry, I couldn't think of a response.")
        print("Gemini Error:", e)

# --- Command Handlers ---
print("  command processing function")
def process_command(command):
    command = command.lower().strip()
    command_handled = False

    if command in ["exit", "quit", "shutdown"]:
        speak("Goodbye!")
        exit()
    if "what" in command:
        if "time" in command:
            time_now = datetime.datetime.now().strftime("%I hours and %M minutes")
            speak(f"The time is {time_now}")
            command_handled = True
    if "find file" in command:
        find_file_command(command, command.index("find file"))
        command_handled = True
    if "open" in command:
        open_commands(command, command.index("open"))
        command_handled = True
    if "play" in command:
        play_command(command, command.index("play"))
        command_handled = True
    if "search" in command:
        search_command(command, command.index("search"))
        command_handled = True

    if not command_handled:
        ask_gemini(command)

print("  file search")
def find_file_command(command, idx):
    command = command[idx:].replace("find file", "").strip()
    command = command.replace(" dot ", ".")
    try:
        path = find_file_and_get_absolute_path(command, "C:/Users/proda/")
        if path:
            os.startfile(path)
        else:
            speak("File not found")
    except Exception as e:
        speak("Error opening the file")
        print("File Error:", e)

def find_file_and_get_absolute_path(filename, search_directory):
    for root, dirs, files in os.walk(search_directory):
        if filename in files:
            return os.path.join(root, filename)
    return None

print("  google search command")
def search_command(command, idx):
    command = command[idx:].replace("search", "", 1).strip()
    webbrowser.open("https://www.google.com/search?q=" + command)
    speak("Here you go")

print("  play commands")
def play_command(command, idx):
    command = command[idx:].lower().replace("play", "", 1).strip()
    for item in musicLibrary.music:
        if item in command:
            webbrowser.open(musicLibrary.music[item])
            speak("Here you go")
            return
    webbrowser.open("https://www.youtube.com/results?search_query=" + command)
    speak("Here are some choices on YouTube")

print("  open commands")
def open_commands(command, idx):
    command = command[idx:].replace("open", "", 1).strip()
    for key in trigger.trigger_word:
        if all(word in command for word in trigger.trigger_word[key]):
            webbrowser.open(key)
            speak("Opening " + " ".join(trigger.trigger_word[key]))
            for i in trigger.trigger_word[key]:
                command = command.replace(i, "", 1)

print("[System]: functions loaded\n")


# --- Continuous Background Listener ---
def callback(recognizer, audio):
    try:
        text = recognizer.recognize_google(audio)
        print("You:", text)
        if "friday" in text.lower():
            text = text.lower().replace("friday", "").strip()
            process_command(text)
    except sr.UnknownValueError:
        pass  # Silence is ignored
    except Exception as e:
        print("Callback Error:", e)

try:
    mic = sr.Microphone(device_index=None)
    with mic as source:
        recognizer.adjust_for_ambient_noise(source, duration=2)
        recognizer.energy_threshold = 300

    print("[Friday]: Listening in background...")
    stop_listening = recognizer.listen_in_background(mic, callback)

    # Keep main thread alive
    while True:
        time.sleep(0.1)

except Exception as e:
    print("Fatal Error:", e)

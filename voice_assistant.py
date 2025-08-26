"""
Simple Voice Assistant (Windows-friendly)
Updated with extra commands:
- Shutdown PC
- Open Instagram login
- Open Gmail
- Open WhatsApp Desktop
- Open ChatGPT in Chrome
- Open VS Code
- Take Screenshot
- Chrome controls (new tab, close chrome, bookmarks)
"""

import speech_recognition as sr
import webbrowser
import subprocess
import os
import platform
import re
import time
from urllib.parse import quote_plus
import pyautogui  # for screenshot and Chrome shortcuts

try:
    import pyttsx3
    TTS_AVAILABLE = True
    tts_engine = pyttsx3.init()
except Exception:
    TTS_AVAILABLE = False
    tts_engine = None

# Change language here if you prefer Hindi recognition (hi-IN) or English (en-IN/en-US)
LANGUAGE = "en-IN"   # try "hi-IN" for Hindi, or "en-US"

def speak(text):
    print("[Assistant]:", text)
    if TTS_AVAILABLE:
        try:
            tts_engine.say(text)
            tts_engine.runAndWait()
        except Exception as e:
            print("TTS error:", e)

# ------------------ Helper Commands ------------------ #

def open_whatsapp():
    url = "https://web.whatsapp.com/"
    webbrowser.open(url)
    speak("Opening WhatsApp Web")

def open_whatsapp_desktop():
    try:
        subprocess.Popen([r"C:\Users\%USERNAME%\AppData\Local\WhatsApp\WhatsApp.exe"])
        speak("Opening WhatsApp Desktop")
    except Exception:
        speak("WhatsApp Desktop not found, opening WhatsApp Web instead")
        open_whatsapp()

def open_cmd():
    system = platform.system()
    try:
        if system == "Windows":
            subprocess.Popen(["cmd.exe"])
        elif system == "Linux":
            subprocess.Popen(["x-terminal-emulator"])
        elif system == "Darwin":
            subprocess.Popen(["/Applications/Utilities/Terminal.app/Contents/MacOS/Terminal"])
        else:
            speak("Unsupported OS for opening cmd automatically.")
            return
        speak("Opening command prompt")
    except Exception as e:
        speak(f"Failed to open command prompt: {e}")

def open_notepad():
    try:
        subprocess.Popen(["notepad.exe"])
        speak("Opening Notepad")
    except Exception as e:
        speak(f"Failed to open notepad: {e}")

def open_explorer():
    try:
        subprocess.Popen(["explorer"])
        speak("Opening File Explorer")
    except Exception as e:
        speak(f"Failed to open file manager: {e}")

def open_chrome():
    try:
        chrome_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
        ]
        for p in chrome_paths:
            if os.path.exists(p):
                subprocess.Popen([p])
                speak("Opening Google Chrome")
                return
        webbrowser.open("https://www.google.com")
        speak("Opening browser")
    except Exception as e:
        speak(f"Failed to open Chrome: {e}")

def search_google(query):
    if not query:
        speak("Query missing.")
        return
    url = "https://www.google.com/search?q=" + quote_plus(query)
    webbrowser.open(url)
    speak(f"Searching Google for {query}")

def shutdown_pc():
    speak("Shutting down your computer")
    os.system("shutdown /s /t 1")

def open_instagram():
    webbrowser.open("https://www.instagram.com/accounts/login/")
    speak("Opening Instagram login page")

def open_gmail():
    webbrowser.open("https://mail.google.com/")
    speak("Opening Gmail")

def open_gpt():
    webbrowser.open("https://chat.openai.com/")
    speak("Opening ChatGPT")

def open_vscode():
    try:
        subprocess.Popen(["code"])
        speak("Opening Visual Studio Code")
    except Exception:
        speak("VS Code not found in PATH")

def take_screenshot():
    img = pyautogui.screenshot()
    img.save("screenshot.png")
    speak("Screenshot saved as screenshot.png")

def chrome_new_tab():
    pyautogui.hotkey("ctrl", "t")
    speak("Opened a new tab in Chrome")

def chrome_close():
    pyautogui.hotkey("ctrl", "shift", "w")
    speak("Closed Chrome window")

def chrome_bookmarks():
    pyautogui.hotkey("ctrl", "shift", "o")
    speak("Opening Chrome bookmarks")

# ------------------ Parse and Execute ------------------ #

def parse_and_execute(text):
    t = text.lower().strip()
    print("Parsed text ->", t)

    # Exit commands
    if any(x in t for x in ["exit", "quit", "bye", "stop assistant", "shut down assistant", "stop"]):
        speak("Goodbye! Stopping assistant.")
        return "exit"

    # Shutdown PC
    if "shutdown" in t:
        shutdown_pc()
        return

    # WhatsApp
    if "whatsapp" in t and "web" not in t:
        open_whatsapp_desktop()
        return
    if "whatsapp web" in t:
        open_whatsapp()
        return

    # Command Prompt
    if "cmd" in t or "command prompt" in t:
        open_cmd()
        return

    # Notepad
    if "notepad" in t or "text editor" in t:
        open_notepad()
        return

    # File Explorer
    if "explorer" in t or "file manager" in t or "file explorer" in t:
        open_explorer()
        return

    # Chrome / browser
    if "chrome" in t or "browser" in t:
        open_chrome()
        return

    # Instagram
    if "instagram" in t or "insta" in t:
        open_instagram()
        return

    # Gmail
    if "gmail" in t or "email" in t:
        open_gmail()
        return

    # ChatGPT
    if "chat gpt" in t or "gpt" in t:
        open_gpt()
        return

    # VS Code
    if "code" in t or "vscode" in t or "visual studio code" in t:
        open_vscode()
        return

    # Screenshot
    if "screenshot" in t:
        take_screenshot()
        return

    # Chrome Controls
    if "new tab" in t:
        chrome_new_tab()
        return
    if "close chrome" in t:
        chrome_close()
        return
    if "bookmarks" in t:
        chrome_bookmarks()
        return

    # Search Google
    query = None
    m = re.search(r"search (for )?(on google )?(?P<q>.+)", t)
    if m:
        query = m.group("q")
    else:
        m2 = re.search(r"google (?P<q>.+)", t)
        if m2:
            query = m2.group("q")
        elif t.startswith("search"):
            query = t[len("search"):].strip()

    if query:
        query = re.sub(r"\bplease\b", "", query).strip()
        search_google(query)
        return

    # Default
    speak("Sorry, command not recognized.")

# ------------------ Main Loop ------------------ #

def main_loop():
    recognizer = sr.Recognizer()
    try:
        mic = sr.Microphone()
    except Exception as e:
        print("Microphone error:", e)
        return

    with mic as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
    speak("Assistant is ready. Say a command.")

    while True:
        try:
            with mic as source:
                print("Listening...")
                audio = recognizer.listen(source, phrase_time_limit=6)
            try:
                text = recognizer.recognize_google(audio, language=LANGUAGE)
            except sr.UnknownValueError:
                try:
                    text = recognizer.recognize_google(audio, language="hi-IN")
                except Exception:
                    raise
            print("You said:", text)
            result = parse_and_execute(text)
            if result == "exit":
                break
        except sr.UnknownValueError:
            print("Didn't catch that.")
        except sr.RequestError as e:
            print("Google Speech API error:", e)
        except KeyboardInterrupt:
            print("Stopped by user.")
            break
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    main_loop()







"""
Simple Voice Assistant (Windows-friendly)

Features:
- Listen to your voice (using microphone) and run simple commands:
    * "open whatsapp" / "whatsapp khol" -> opens WhatsApp Web
    * "open cmd" / "open command prompt" -> opens Command Prompt
    * "search ..." / "search for ..." / "google ..." -> opens Google search for the query
    * "open notepad", "open explorer", "open chrome" etc.
    * "exit" / "quit" / "stop" -> stops assistant

Notes:
- Uses the Google Web Speech API via SpeechRecognition (requires internet).
- On Windows you'll likely need PyAudio. If pip install pyaudio fails, use:
    pip install pipwin
    pipwin install pyaudio

Before running: pip install -r requirements.txt
Run: python voice_assistant.py


import speech_recognition as sr
import webbrowser
import subprocess
import os
import platform
import re
import time
from urllib.parse import quote_plus

try:
    import pyttsx3
    TTS_AVAILABLE = True
    tts_engine = pyttsx3.init()
except Exception:
    TTS_AVAILABLE = False
    tts_engine = None

# Change language here if you prefer Hindi recognition (hi-IN) or English (en-IN/en-US)
LANGUAGE = "en-IN"   # try "hi-IN" for Hindi, or "en-US"

def speak(text):
    print("[Assistant]:", text)
    if TTS_AVAILABLE:
        try:
            tts_engine.say(text)
            tts_engine.runAndWait()
        except Exception as e:
            print("TTS error:", e)

def open_whatsapp():
    url = "https://web.whatsapp.com/"
    webbrowser.open(url)
    speak("Opening WhatsApp Web")

def open_cmd():
    system = platform.system()
    try:
        if system == "Windows":
            # open a new cmd window
            subprocess.Popen(["cmd.exe"])
        elif system == "Linux":
            subprocess.Popen(["x-terminal-emulator"])
        elif system == "Darwin":
            subprocess.Popen(["/Applications/Utilities/Terminal.app/Contents/MacOS/Terminal"])
        else:
            speak("Unsupported OS for opening cmd automatically.")
            return
        speak("Opening command prompt")
    except Exception as e:
        speak(f"Failed to open command prompt: {e}")

def open_notepad():
    system = platform.system()
    try:
        if system == "Windows":
            subprocess.Popen(["notepad.exe"])
            speak("Opening Notepad")
        elif system == "Linux":
            subprocess.Popen(["gedit"])
            speak("Opening editor")
        else:
            speak("Not supported on this OS.")
    except Exception as e:
        speak(f"Failed to open notepad/editor: {e}")

def open_explorer():
    system = platform.system()
    try:
        if system == "Windows":
            subprocess.Popen(["explorer"])
            speak("Opening File Explorer")
        elif system == "Linux":
            subprocess.Popen(["xdg-open", "."])
            speak("Opening file manager")
        else:
            speak("Not supported on this OS.")
    except Exception as e:
        speak(f"Failed to open file manager: {e}")

def open_chrome():
    try:
        # This will open the default browser; try to open chrome specifically if present
        chrome_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
        ]
        for p in chrome_paths:
            if os.path.exists(p):
                subprocess.Popen([p])
                speak("Opening Google Chrome")
                return
        # fallback: open default browser
        webbrowser.open("https://www.google.com")
        speak("Opening browser")
    except Exception as e:
        speak(f"Failed to open Chrome: {e}")

def search_google(query):
    if not query:
        speak("Query missing.")
        return
    url = "https://www.google.com/search?q=" + quote_plus(query)
    webbrowser.open(url)
    speak(f"Searching Google for {query}")

def parse_and_execute(text):
    t = text.lower().strip()
    print("Parsed text ->", t)
    # Exit commands
    if any(x in t for x in ["exit", "quit", "bye", "stop assistant", "shut down", "shutdown", "stop"]):
        speak("Goodbye! Stopping assistant.")
        return "exit"

    # WhatsApp
    if "whatsapp" in t:
        open_whatsapp()
        return

    # Command Prompt / CMD
    if "cmd" in t or "command prompt" in t or "commandprompt" in t:
        open_cmd()
        return

    # Notepad
    if "notepad" in t or "text editor" in t:
        open_notepad()
        return

    # Explorer / file manager
    if "explorer" in t or "file explorer" in t or "file manager" in t or "open files" in t:
        open_explorer()
        return

    # Chrome / browser
    if "chrome" in t or "browser" in t:
        open_chrome()
        return

    # Search commands: look for 'search', 'search for', or 'google'
    # Try patterns in order
    query = None
    m = re.search(r"search (for )?(on google )?(?P<q>.+)", t)
    if m:
        query = m.group("q")
    else:
        m2 = re.search(r"google (?P<q>.+)", t)
        if m2:
            query = m2.group("q")
        else:
            # fallback: if phrase starts with 'search' but didn't match above
            if t.startswith("search"):
                query = t[len("search"):].strip()
    if query:
        # clean trailing words like 'please'
        query = re.sub(r"\bplease\b", "", query).strip()
        search_google(query)
        return

    # If nothing matched:
    speak("Sorry, command not recognized. Try: open whatsapp, open cmd, search something on google, open notepad, open chrome, or say 'exit' to stop.")

def main_loop():
    recognizer = sr.Recognizer()
    mic = None
    try:
        mic = sr.Microphone()
    except Exception as e:
        print("No microphone found or PyAudio not installed. Please ensure microphone is connected and PyAudio is installed.")
        print("Detailed error:", e)
        return

    with mic as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
    speak("Assistant is ready. Say a command clearly after the beep.")
    time.sleep(0.5)
    while True:
        try:
            with mic as source:
                print("Listening... (speak now)")
                audio = recognizer.listen(source, phrase_time_limit=6)
            try:
                # try English first (or whatever LANGUAGE is set)
                text = recognizer.recognize_google(audio, language=LANGUAGE)
            except sr.UnknownValueError:
                # try Hindi if English didn't work (common with mixed language)
                try:
                    text = recognizer.recognize_google(audio, language="hi-IN")
                except Exception:
                    raise
            print("You said:", text)
            result = parse_and_execute(text)
            if result == "exit":
                break
        except sr.UnknownValueError:
            print("Didn't catch that. Please speak clearly.")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; check your internet connection.")
            print("Error:", e)
        except KeyboardInterrupt:
            print("Interrupted by user. Exiting.")
            break
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    main_loop()
"""
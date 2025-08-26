# Simple Voice Assistant (Windows-friendly)

**Zip contents**
- `voice_assistant.py` — main Python script
- `requirements.txt` — Python packages to install
- `README.md` — this file (instructions)

---

## Quick Hindi instructions (sadhaaran aur seedha)

1. **Python install karo** — Python 3.8 ya upar. (https://www.python.org se install karo)
2. Zip file extract karo.
3. Command Prompt khol ke folder me jao (jahan `voice_assistant.py` hai).
4. (Optional but recommended) Virtual environment banao:
   ```
   python -m venv venv
   venv\Scripts\activate
   ```
5. Dependencies install karo:
   ```
   pip install -r requirements.txt
   ```
   - Agar `pyaudio` install karne me problem aaye (Windows par kabhi hota hai), tab:
     ```
     pip install pipwin
     pipwin install pyaudio
     ```
6. Microphone permission allow karo (Windows Settings → Microphone).
7. Script run karo:
   ```
   python voice_assistant.py
   ```
8. Bol kar commands do, jaise:
   - "open whatsapp" ya "whatsapp khol"
   - "open cmd" ya "open command prompt"
   - "search how to make biryani" ya "search for nearest restaurant"
   - "open notepad", "open chrome", "open explorer","login insta on google"
   - "exit" ya "quit" to stop

---

## Quick English summary

- The assistant listens using your microphone and uses Google's free speech-to-text (requires internet).
- It performs simple actions: opens websites, opens apps like cmd/notepad, and runs Google searches in your browser.
- If TTS (text-to-speech) is available (`pyttsx3`), it will speak back confirmations; otherwise it will print messages.

---

## Troubleshooting

- **No microphone detected / PyAudio error**: Install PyAudio with `pipwin` (Windows):
  ```
  pip install pipwin
  pipwin install pyaudio
  ```
- **Speech not recognized reliably**: Speak clearly and try reducing background noise.
- **Google recognizer errors**: Ensure you are online. The script uses Google's free web API and may return `RequestError` if internet is down.
- **Permissions**: Windows → Settings → Privacy → Microphone → Allow apps access.

---

## Customize commands

Open `voice_assistant.py` and edit `parse_and_execute` to add or change commands and actions.

---

If you want, I can add more specific commands (like "open WhatsApp Desktop" if installed, or controlling other apps). Tell me which exact actions you want and I will update the package.
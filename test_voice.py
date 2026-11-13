"""Hear Adrienne's voice without needing any API key. Run: python test_voice.py"""
import json
from pathlib import Path

import pyttsx3

cfg_path = Path(__file__).parent / "config.json"
cfg = json.loads(cfg_path.read_text()) if cfg_path.exists() else {}
phrase = cfg.get("wake_response", "Yes?")

tts = pyttsx3.init()
voices = tts.getProperty("voices")

print("Voices installed on this PC:")
for i, v in enumerate(voices):
    print(f"  {i}: {v.name}")

for want in [cfg.get("voice_name", "Zira"), "Zira", "Hazel", "Susan", "Eva", "Aria", "Jenny"]:
    match = next((v for v in voices if want.lower() in v.name.lower()), None)
    if match:
        tts.setProperty("voice", match.id)
        print(f"\nSpeaking with: {match.name}")
        break

tts.setProperty("rate", cfg.get("voice_rate", 175))
tts.say(phrase)
tts.runAndWait()

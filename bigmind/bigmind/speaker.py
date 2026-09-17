"""Síntese de voz: converte texto em fala (offline, via pyttsx3)."""

import pyttsx3


class Speaker:
    def __init__(self, rate: int = 175, volume: float = 1.0, voice_hint: str = "brazil"):
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", rate)
        self.engine.setProperty("volume", volume)

        # Tenta escolher uma voz em português, se existir instalada no sistema.
        for voice in self.engine.getProperty("voices"):
            name = (voice.name or "").lower()
            vid = (voice.id or "").lower()
            if voice_hint in name or "portuguese" in name or "pt" in vid:
                self.engine.setProperty("voice", voice.id)
                break

    def say(self, text: str):
        print(f"🤖 BigMind: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

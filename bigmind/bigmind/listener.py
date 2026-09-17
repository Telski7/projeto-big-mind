"""Reconhecimento de voz: converte fala do microfone em texto."""

import speech_recognition as sr


class Listener:
    def __init__(self, language: str = "pt-BR"):
        self.recognizer = sr.Recognizer()
        self.language = language
        self.microphone = sr.Microphone()
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)

    def listen(self) -> str | None:
        """Escuta o microfone e retorna o texto reconhecido, ou None se falhar."""
        with self.microphone as source:
            print("🎙️  Ouvindo...")
            try:
                audio = self.recognizer.listen(source, timeout=6, phrase_time_limit=12)
            except sr.WaitTimeoutError:
                return None

        try:
            text = self.recognizer.recognize_google(audio, language=self.language)
            print(f"👤 Você: {text}")
            return text
        except sr.UnknownValueError:
            print("🤔 Não entendi o áudio.")
            return None
        except sr.RequestError as e:
            print(f"⚠️  Erro no serviço de reconhecimento: {e}")
            return None

"""BigMind — ponto de entrada.

Uso:
    python main.py            # modo voz (fala/escuta)
    python main.py --text     # modo texto (teclado)
"""

import sys

from bigmind import config, memory, brain


def run_text_mode():
    print(f"=== {config.ASSISTANT_NAME} (modo texto) ===")
    print("Digite 'sair' para encerrar.\n")
    while True:
        try:
            user_text = input("Você: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nAté mais!")
            break
        if not user_text:
            continue
        if user_text.lower() in {"sair", "exit", "quit"}:
            print(f"{config.ASSISTANT_NAME}: Até logo!")
            break
        reply = brain.respond(user_text)
        print(f"{config.ASSISTANT_NAME}: {reply}")


def run_voice_mode():
    from bigmind.listener import Listener
    from bigmind.speaker import Speaker

    listener = Listener()
    speaker = Speaker()

    print(f"=== {config.ASSISTANT_NAME} (modo voz) ===")
    speaker.say(f"{config.ASSISTANT_NAME} ativado. Pode falar.")

    while True:
        try:
            text = listener.listen()
        except KeyboardInterrupt:
            speaker.say("Até logo!")
            break

        if not text:
            continue
        if text.lower() in {"sair", "encerrar", "tchau", "pare"}:
            speaker.say("Até logo!")
            break

        reply = brain.respond(text)
        speaker.say(reply)


if __name__ == "__main__":
    memory.init_db()

    if "--text" in sys.argv:
        run_text_mode()
    else:
        try:
            run_voice_mode()
        except Exception as e:
            print(f"[BigMind] Não consegui iniciar o modo voz ({e}).")
            print("Verifique se microfone/pyaudio estão instalados, ou use: python main.py --text")

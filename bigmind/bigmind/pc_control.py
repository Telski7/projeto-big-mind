"""Comandos de controle do computador (multiplataforma, com fallback gracioso)."""

import os
import platform
import subprocess
import webbrowser
from datetime import datetime

SYSTEM = platform.system()  # "Windows", "Darwin" (mac), "Linux"


def open_app(app_name: str) -> str:
    """Abre um programa/site comum pelo nome falado."""
    app_name = app_name.lower().strip()

    sites = {
        "youtube": "https://youtube.com",
        "google": "https://google.com",
        "gmail": "https://mail.google.com",
        "whatsapp": "https://web.whatsapp.com",
    }
    if app_name in sites:
        webbrowser.open(sites[app_name])
        return f"Abrindo {app_name}."

    apps = {
        "navegador": {
            "Windows": "start chrome",
            "Darwin": "open -a 'Google Chrome'",
            "Linux": "xdg-open https://google.com",
        },
        "bloco de notas": {
            "Windows": "start notepad",
            "Darwin": "open -a TextEdit",
            "Linux": "gedit",
        },
        "calculadora": {
            "Windows": "start calc",
            "Darwin": "open -a Calculator",
            "Linux": "gnome-calculator",
        },
        "terminal": {
            "Windows": "start cmd",
            "Darwin": "open -a Terminal",
            "Linux": "x-terminal-emulator",
        },
    }

    if app_name in apps and SYSTEM in apps[app_name]:
        try:
            subprocess.Popen(apps[app_name][SYSTEM], shell=True)
            return f"Abrindo {app_name}."
        except Exception as e:
            return f"Não consegui abrir {app_name}: {e}"

    return f"Ainda não sei abrir '{app_name}'. Você pode ensinar essa função em pc_control.py."


def set_volume(level: int) -> str:
    """Define o volume do sistema (0-100). Requer pycaw no Windows."""
    level = max(0, min(100, level))
    try:
        if SYSTEM == "Windows":
            from ctypes import cast, POINTER
            from comtypes import CLSCTX_ALL
            from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            volume.SetMasterVolumeLevelScalar(level / 100, None)
        elif SYSTEM == "Darwin":
            subprocess.run(["osascript", "-e", f"set volume output volume {level}"])
        else:  # Linux
            subprocess.run(["amixer", "-D", "pulse", "sset", "Master", f"{level}%"])
        return f"Volume ajustado para {level}%."
    except Exception as e:
        return f"Não consegui ajustar o volume ({e}). Verifique as dependências opcionais do requirements.txt."


def mute() -> str:
    return set_volume(0)


def take_screenshot(save_dir: str = ".") -> str:
    try:
        import pyautogui

        filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        path = os.path.join(save_dir, filename)
        pyautogui.screenshot().save(path)
        return f"Print salvo em {path}."
    except Exception as e:
        return f"Não consegui tirar o print ({e}). Instale 'pyautogui'."


def lock_screen() -> str:
    try:
        if SYSTEM == "Windows":
            subprocess.run(["rundll32.exe", "user32.dll,LockWorkStation"])
        elif SYSTEM == "Darwin":
            subprocess.run(
                ["/System/Library/CoreServices/Menu Extras/User.menu/Contents/Resources/CGSession", "-suspend"]
            )
        else:
            subprocess.run(["loginctl", "lock-session"])
        return "Tela bloqueada."
    except Exception as e:
        return f"Não consegui bloquear a tela ({e})."


def shutdown(confirm: bool = False) -> str:
    if not confirm:
        return "Tem certeza que quer desligar o computador? Diga 'confirmar desligamento' para prosseguir."
    try:
        if SYSTEM == "Windows":
            subprocess.run(["shutdown", "/s", "/t", "5"])
        else:
            subprocess.run(["shutdown", "-h", "now"])
        return "Desligando o computador."
    except Exception as e:
        return f"Não consegui desligar ({e})."

"""Integração com TVs.

Por padrão usa Chromecast (funciona com qualquer TV/dongle/Android TV
na mesma rede). Há esqueletos comentados para Samsung (Tizen) e LG
(webOS) — descomente e configure o TV_IP no .env se for o seu caso.
"""

from . import config


def _get_chromecast():
    import pychromecast

    chromecasts, browser = pychromecast.get_chromecasts()
    if not chromecasts:
        return None, browser
    cast = chromecasts[0]
    cast.wait()
    return cast, browser


def cast_media(url: str, content_type: str = "video/mp4") -> str:
    """Joga uma mídia (link direto de vídeo/imagem) na TV via Chromecast."""
    try:
        cast, browser = _get_chromecast()
        if cast is None:
            return "Nenhum Chromecast encontrado na rede."
        mc = cast.media_controller
        mc.play_media(url, content_type)
        mc.block_until_active()
        browser.stop_discovery()
        return "Jogando na TV."
    except Exception as e:
        return f"Não consegui conectar na TV ({e}). Verifique se está na mesma rede Wi-Fi."


def pause() -> str:
    try:
        cast, browser = _get_chromecast()
        if cast is None:
            return "Nenhum Chromecast encontrado."
        cast.media_controller.pause()
        browser.stop_discovery()
        return "Pausado."
    except Exception as e:
        return f"Erro ao pausar ({e})."


def play() -> str:
    try:
        cast, browser = _get_chromecast()
        if cast is None:
            return "Nenhum Chromecast encontrado."
        cast.media_controller.play()
        browser.stop_discovery()
        return "Retomando."
    except Exception as e:
        return f"Erro ao retomar ({e})."


def set_tv_volume(level: int) -> str:
    """Volume de 0 a 100 (Chromecast usa escala 0.0-1.0 internamente)."""
    try:
        cast, browser = _get_chromecast()
        if cast is None:
            return "Nenhum Chromecast encontrado."
        cast.set_volume(max(0, min(100, level)) / 100)
        browser.stop_discovery()
        return f"Volume da TV ajustado para {level}%."
    except Exception as e:
        return f"Erro ao ajustar volume da TV ({e})."


# ---------------------------------------------------------------------------
# Esqueleto para Samsung (Tizen) — requer `pip install samsungtvws`
# ---------------------------------------------------------------------------
# from samsungtvws import SamsungTVWS
#
# def samsung_send_key(key: str) -> str:
#     tv = SamsungTVWS(host=config.TV_IP)
#     tv.send_key(key)  # ex: "KEY_VOLUP", "KEY_POWER", "KEY_HOME"
#     return f"Comando {key} enviado para a TV Samsung."


# ---------------------------------------------------------------------------
# Esqueleto para LG (webOS) — requer `pip install pywebostv`
# ---------------------------------------------------------------------------
# from pywebostv.connection import WebOSClient
# from pywebostv.controls import MediaControl, SystemControl
#
# def lg_connect():
#     client = WebOSClient(config.TV_IP)
#     client.connect()
#     for status in client.register({}):
#         pass  # na primeira vez, aceite o pareamento na tela da TV
#     return client

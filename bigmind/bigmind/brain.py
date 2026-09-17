"""Lógica de conversa: roteia comandos diretos e conversa livre com o Claude."""

import re

from anthropic import Anthropic

from . import config, memory, pc_control, tv_control

_client = Anthropic(api_key=config.ANTHROPIC_API_KEY) if config.ANTHROPIC_API_KEY else None

SYSTEM_PROMPT = f"""Você é {config.ASSISTANT_NAME}, um assistente pessoal estilo Jarvis.
Responda sempre em português do Brasil, de forma direta, natural e um pouco espirituosa,
como um bom assistente pessoal. Seja conciso — respostas de voz devem ser curtas.
Você tem memória das conversas anteriores com o usuário; use-a quando for relevante,
mas não fique repetindo o que já sabe sem necessidade."""


def _try_handle_command(text: str) -> str | None:
    """Tenta interpretar `text` como um comando direto de PC/TV.
    Retorna a resposta se reconheceu o comando, ou None para cair na conversa livre."""
    t = text.lower().strip()

    # --- PC ---
    m = re.search(r"abrir?\s+(.+)", t)
    if m and any(k in t for k in ["navegador", "bloco de notas", "calculadora", "terminal",
                                    "youtube", "google", "gmail", "whatsapp"]):
        return pc_control.open_app(m.group(1))

    if "aumentar volume" in t or "sobe o volume" in t or "sobe volume" in t:
        return pc_control.set_volume(80)
    if "diminuir volume" in t or "abaixa o volume" in t or "abaixa volume" in t:
        return pc_control.set_volume(20)
    if "mudo" in t or "silenciar" in t:
        return pc_control.mute()
    m = re.search(r"volume\s+(?:para\s+)?(\d+)", t)
    if m and "tv" not in t:
        return pc_control.set_volume(int(m.group(1)))

    if "print" in t or "screenshot" in t or "captura de tela" in t:
        return pc_control.take_screenshot()

    if "bloquear tela" in t or "bloqueia a tela" in t:
        return pc_control.lock_screen()

    if "confirmar desligamento" in t:
        return pc_control.shutdown(confirm=True)
    if "desligar computador" in t or "desligar o pc" in t:
        return pc_control.shutdown(confirm=False)

    # --- TV ---
    m = re.search(r"jogar?\s+(.+?)\s+na\s+tv", t)
    if m:
        return tv_control.cast_media(m.group(1).strip())
    if "pausar tv" in t or "pausa a tv" in t:
        return tv_control.pause()
    if "tocar tv" in t or "retomar tv" in t or "play na tv" in t:
        return tv_control.play()
    m = re.search(r"tv\s+volume\s+(\d+)", t)
    if m:
        return tv_control.set_tv_volume(int(m.group(1)))

    # --- Memória ---
    m = re.search(r"lembr(?:e|a)-?te\s+(?:que\s+)?(.+)", t)
    if m:
        memory.save_fact(m.group(1).strip())
        return "Anotado, vou lembrar disso."
    if "esquece o que a gente conversou" in t or "limpar histórico" in t:
        memory.clear_history()
        return "Histórico de conversa apagado. Mas os fatos que você me pediu para lembrar continuam salvos."

    return None


def respond(user_text: str) -> str:
    """Processa a entrada do usuário: tenta comando direto, senão conversa com o Claude."""
    memory.save_message("user", user_text)

    command_reply = _try_handle_command(user_text)
    if command_reply is not None:
        memory.save_message("assistant", command_reply)
        return command_reply

    if _client is None:
        reply = (
            "Minha chave da API da Anthropic não está configurada. "
            "Edite o arquivo .env e adicione sua ANTHROPIC_API_KEY."
        )
        memory.save_message("assistant", reply)
        return reply

    history = memory.get_recent_messages(limit=20)
    facts = memory.get_all_facts()

    system = SYSTEM_PROMPT
    if facts:
        bullet_facts = "\n".join(f"- {f}" for f in facts)
        system += f"\n\nFatos que o usuário pediu para você lembrar permanentemente:\n{bullet_facts}"

    try:
        response = _client.messages.create(
            model=config.MODEL,
            max_tokens=500,
            system=system,
            messages=history,
        )
        reply = "".join(block.text for block in response.content if block.type == "text").strip()
    except Exception as e:
        reply = f"Tive um problema para pensar na resposta: {e}"

    memory.save_message("assistant", reply)
    return reply

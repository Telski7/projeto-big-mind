"""Carrega configurações do .env."""

import os
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
ASSISTANT_NAME = os.getenv("BIGMIND_NAME", "BigMind")
MODEL = os.getenv("BIGMIND_MODEL", "claude-sonnet-4-5")
TV_IP = os.getenv("TV_IP", "")

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "bigmind_memory.db")

if not ANTHROPIC_API_KEY:
    print(
        "[BigMind] Aviso: ANTHROPIC_API_KEY não configurada. "
        "Copie .env.example para .env e preencha sua chave."
    )

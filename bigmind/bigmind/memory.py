"""Memória persistente das conversas, usando SQLite.

Guarda cada mensagem (usuário/assistente) com timestamp, e permite
recuperar o histórico recente para dar contexto ao Claude, além de
guardar "fatos" marcantes que o usuário pediu para lembrar.
"""

import sqlite3
from datetime import datetime, timezone
from contextlib import contextmanager

from . import config


@contextmanager
def _connect():
    conn = sqlite3.connect(config.DB_PATH)
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db():
    with _connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS facts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )


def save_message(role: str, content: str):
    with _connect() as conn:
        conn.execute(
            "INSERT INTO messages (role, content, created_at) VALUES (?, ?, ?)",
            (role, content, datetime.now(timezone.utc).isoformat()),
        )


def get_recent_messages(limit: int = 20):
    """Retorna as últimas `limit` mensagens, em ordem cronológica,
    prontas para entrar em `messages=[...]` na chamada da API."""
    with _connect() as conn:
        rows = conn.execute(
            "SELECT role, content FROM messages ORDER BY id DESC LIMIT ?",
            (limit,),
        ).fetchall()
    rows.reverse()
    return [{"role": role, "content": content} for role, content in rows]


def save_fact(content: str):
    with _connect() as conn:
        conn.execute(
            "INSERT INTO facts (content, created_at) VALUES (?, ?)",
            (content, datetime.now(timezone.utc).isoformat()),
        )


def get_all_facts():
    with _connect() as conn:
        rows = conn.execute("SELECT content FROM facts ORDER BY id ASC").fetchall()
    return [r[0] for r in rows]


def clear_history():
    """Apaga o histórico de mensagens (mantém os fatos salvos)."""
    with _connect() as conn:
        conn.execute("DELETE FROM messages")

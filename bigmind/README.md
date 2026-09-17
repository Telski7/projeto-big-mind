# BigMind 🧠

Assistente virtual pessoal estilo Jarvis, com:

- 🎙️ Conversa por voz (fala e escuta)
- 🧠 Memória persistente das conversas (SQLite — ele "lembra" o que você falou antes)
- 💻 Controle do PC (abrir programas, volume, screenshot, bloquear tela, desligar)
- 📺 Integração com TV (Chromecast nativo; ganchos prontos para Samsung/LG)
- 🤖 Cérebro baseado na API da Anthropic (Claude)

## Estrutura

```
bigmind/
├── main.py                  # Ponto de entrada (loop principal)
├── requirements.txt
├── .env.example              # Modelo das variáveis de ambiente
├── bigmind/
│   ├── __init__.py
│   ├── config.py             # Carrega configurações e chaves
│   ├── memory.py             # Memória persistente em SQLite
│   ├── listener.py           # Reconhecimento de voz (fala → texto)
│   ├── speaker.py            # Síntese de voz (texto → fala)
│   ├── brain.py              # Lógica de conversa (chama a API do Claude)
│   ├── pc_control.py         # Comandos para controlar o computador
│   └── tv_control.py         # Comandos para controlar a TV
```

## Instalação

```bash
git clone https://github.com/SEU_USUARIO/bigmind.git
cd bigmind
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

Edite o `.env` e coloque sua chave da API da Anthropic:

```
ANTHROPIC_API_KEY=sua_chave_aqui
```

## Uso

Modo voz (padrão, precisa de microfone):

```bash
python main.py
```

Modo texto (sem microfone/alto-falante, útil para testar):

```bash
python main.py --text
```

## Comandos especiais reconhecidos

Além de conversar livremente, o BigMind entende comandos diretos (em português), por exemplo:

- "abrir navegador" / "abrir bloco de notas"
- "aumentar volume" / "diminuir volume" / "mudo"
- "tirar print" / "tirar screenshot"
- "bloquear tela"
- "desligar computador" (pede confirmação)
- "jogar [algo] na tv" (cast via Chromecast)
- "pausar tv" / "tv volume 20"

Tudo que não bater com um comando é mandado para o Claude conversar normalmente, com memória das últimas interações.

## Integração com TV

Por padrão usa **Chromecast** (via `pychromecast`), que funciona com qualquer TV/Chromecast/Android TV na mesma rede Wi-Fi.

Para Samsung (Tizen) ou LG (webOS), há esqueletos prontos em `tv_control.py` usando as bibliotecas `samsungtvws` e `pywebostv` — descomente e configure o IP da TV.

## Próximos passos sugeridos

- Trocar o reconhecimento de voz por um wake word local (ex: `porcupine`) para não precisar apertar Enter
- Adicionar mais "skills" (clima, lembretes, agenda)
- Rodar como serviço/daemon no PC (systemd no Linux, Task Scheduler no Windows)

## Licença

MIT — veja `LICENSE`.

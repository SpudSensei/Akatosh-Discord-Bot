# Akatosh — Discord Bot with GPT‑4 (Moderation + Q&A)

Akatosh is a Discord bot that answers questions using OpenAI’s GPT‑4 and provides basic server logs to assist moderation.

> **Do not commit secrets.** Keep your API keys and tokens in a local `.env` file and add it to `.gitignore`.

---

## Features
- **/ask** — Slash command for quick GPT‑4 answers (persona: *Akatosh, Dragon God of Time*).
- **Server log helpers** — Joins/leaves, message edits/deletes, and voice-channel events into a `#bot-log` channel.
- **Prod‑ready structure** — Uses environment variables and a lightweight dependency set.

---

## Prerequisites
- Python 3.10+
- A Discord Application + Bot (Developer Portal)
- OpenAI API key

---

## 1) Create your Discord bot & get tokens
1. Go to the **Discord Developer Portal** → **New Application** → **Bot** → **Add Bot**.
2. Under **Privileged Gateway Intents**, enable **Message Content Intent** (plus Members if you need join/leave logs).
3. Copy the **Bot Token**.
4. On the **OAuth2 → URL Generator** page, check **bot** and **applications.commands**, then grant minimal permissions (e.g., `Send Messages`, `Read Message History`). Copy the invite URL and add the bot to your server.

---

## 2) Get your OpenAI API key
Create/Copy your key from the OpenAI dashboard.

---

## 3) Project setup
Clone your repo, then create a virtual environment and install deps:

```bash
python -m venv venv
# macOS/Linux
source venv/bin/activate
# Windows
venv\Scripts\activate

pip install -r requirements.txt
```

**requirements.txt** (example):
```txt
discord.py>=2.3.2
python-dotenv>=1.0.1
openai>=1.0.0
```

**.gitignore** (minimum):
```gitignore
# Python
__pycache__/
*.pyc

# Env
.env
venv/
```

---

## 4) Configure environment variables
Create a file named `.env` in the project root (do **not** commit this file):

```env
DISCORD_TOKEN=your_discord_bot_token_here
OPENAI_API_KEY=your_openai_api_key_here
```

If you want to change models, set in code or add:
```env
MODEL_NAME=gpt-4
```

---

## 5) Start the bot locally
Run the bot after your virtual environment is activated:

```bash
python bot.py
```

You should see:
```
✅ Logged in as Akatosh#1234 and slash commands synced.
```

If the `#bot-log` channel exists, join/leave, message edits/deletes, and voice events will be posted there automatically.

---

## 6) Ask questions with /ask
In any server/channel where the bot is present:
- Type **/ask** and enter your question.
- Akatosh will reply using GPT‑4.

Example:
> `/ask How do I create a Python virtual environment on Windows?`

---

## Notes & Safety
- **Never expose tokens/keys.** Keep `.env` out of your repo.
- If you accidentally commit a key, **revoke and regenerate** it immediately.
- For production hosting (Railway, Fly.io, Docker, etc.), set env vars in the platform’s dashboard.

---

## Troubleshooting
- **Slash commands not showing?** Wait a minute after first run, or re‑sync by restarting the bot. Ensure you invited with the `applications.commands` scope.
- **Permissions error?** Confirm the bot’s role can view and send messages in target channels.
- **No logs in `#bot-log`?** Create a text channel named `bot-log`, or update `LOG_CHANNEL_NAME` in the code.
- **OpenAI errors?** Check your API key, model name, and account usage/quota.

---

## Folder layout (suggested)
```
.
├── bot.py              # your main bot file
├── requirements.txt
├── .env                # DO NOT COMMIT
├── .gitignore
└── README.md
```

---

## License
MIT (or your choice).


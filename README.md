# Adrienne

**A voice-controlled, agentic AI assistant for Windows, powered by Claude.** Say her name, give her a task, and she plans it, uses tools on your PC, and reports back. Offline speech recognition, a female voice, and a confirmation step before anything is sent or run.

> Status: personal project / early version. Written for Windows 10/11. Not every feature has been tested on every setup, so expect some rough edges and please open an issue if you hit one.

---

## Repository description (for the GitHub "About" box)

> Voice-activated agentic AI assistant for Windows, built on Claude. Offline Whisper speech recognition, wake word, goal mode, web research, memory, scheduled tasks, email/Telegram/Discord/WhatsApp messaging, with permission tiers and a stop hotkey.

**Suggested topics:** `ai-assistant` `claude` `anthropic` `voice-assistant` `agentic-ai` `whisper` `windows` `python` `jarvis` `tool-use`

---

## Features

| Area | What she does |
|---|---|
| **Voice** | Wake word (her name), offline speech-to-text with `faster-whisper`, spoken replies in a female Windows voice |
| **Goal mode** | You state a goal; she writes a plan, works through it with her tools, checks her results, and summarizes |
| **Web** | Searches the web and reads pages (treated as untrusted content) |
| **Workspace** | Writes files and runs Python inside a dedicated `workspace/` folder |
| **Memory** | Remembers facts and preferences you tell her (`memory.json`) |
| **Scheduled tasks** | Runs tasks on her own, once or daily |
| **Reminders** | Spoken reminders at a set time |
| **Music** | Play/pause/next/volume for any player; opens Spotify or YouTube searches |
| **Calendar** | Reads upcoming Google Calendar events (read-only) |
| **Files** | Reads and summarizes txt, md, pdf, docx and code files |
| **Messaging** | Email (SMTP), Telegram (bot), Discord (webhook), WhatsApp (opens the app with the message filled in) |
| **Calls** | Opens the dialer in Windows Phone Link (needs a paired Android phone) |
| **PC control** | Opens apps and websites; runs PowerShell (with your approval) |

### Permission tiers

| Tier | Actions |
|---|---|
| **Automatic** | Thinking, web search/reading, reading files, writing files inside `workspace/`, memory, reminders, scheduling |
| **Needs your "yes"** | Sending email/messages, placing calls, running Python, running PowerShell |
| **Never** | Reading `config.json`, `token.json`, `credentials.json`, `.env`, `memory.json` |

Scheduled tasks run unattended, so anything needing approval is **declined** and written to `pending_actions.txt` for you to review. Every action is logged in `activity.log`.

---

## Requirements

- Windows 10 or 11
- **Python 3.11 or 3.12** (newer versions may not work with the speech libraries)
- A microphone and speakers (for voice mode)
- An Anthropic API key **with credit on the account** (console.anthropic.com)
- Internet (for the Claude API; speech recognition itself is offline after the first model download)

---

## Installation

All commands are for **Command Prompt** unless noted.

### 1. Get the files

```bat
git clone https://github.com/YOUR-USERNAME/adrienne.git C:\Adrienne
cd C:\Adrienne
```

No git? Download the repository as a ZIP, extract it to `C:\Adrienne`, then:

```bat
cd C:\Adrienne
```

### 2. Install Python

1. Download Python 3.11 or 3.12 from https://www.python.org/downloads/
2. On the first installer screen, tick **Add Python to PATH**, then install.
3. Check it:

```bat
python --version
```

### 3. (Recommended) Create a virtual environment

```bat
python -m venv .venv
.venv\Scripts\activate
```

You'll see `(.venv)` at the start of the prompt. Run `.venv\Scripts\activate` again each time you open a new window.

### 4. Install the dependencies

```bat
pip install -r requirements.txt
```

This takes a few minutes. The Google Calendar packages are optional; if one fails, Adrienne still runs.

### 5. Add your Anthropic API key

1. Go to https://console.anthropic.com
2. Open **Plans & Billing** and add a payment method and a small amount of credit (the free evaluation plan has no credit and returns a "credit balance is too low" error).
3. Open **API keys**, click **Create key**, name it `adrienne`, and copy it immediately (it is shown only once).
4. Save it permanently:

```bat
setx ANTHROPIC_API_KEY "paste-your-key-here"
```

5. **Close the window and open a new Command Prompt**, then:

```bat
cd C:\Adrienne
.venv\Scripts\activate
```

To set the key for the current window only (without saving it):

```bat
set ANTHROPIC_API_KEY=paste-your-key-here
```

PowerShell equivalent: `$env:ANTHROPIC_API_KEY = "paste-your-key-here"`

### 6. Create your config

```bat
copy config.example.json config.json
notepad config.json
```

Edit the values (see [Configuration](#configuration)). Keep the quotation marks, commas and brackets exactly as they are. Delete any section you do not use rather than leaving the sample values.

**Never commit `config.json`.** It holds passwords and tokens, and `.gitignore` excludes it.

### 7. Test her voice

```bat
python test_voice.py
```

You should hear a female voice say your `wake_response`. The script also prints every voice installed on your PC. To add more voices: Settings, Time & language, Speech, Add voices.

---

## Running Adrienne

### Text mode (start here)

```bat
python assistant.py
```

Try:

```
what time is it?
remind me in 2 minutes to drink water
open notepad
```

Type `exit` to quit.

### Voice mode

First allow microphone access: Settings, Privacy & security, Microphone, **Let desktop apps access your microphone**.

```bat
python assistant.py --voice
```

The first launch downloads the Whisper model (internet needed once). When you see `(waiting for 'Adrienne')`, say:

- "Adrienne, what's the time?" (she answers directly)
- "Adrienne" (she replies with your `wake_response`, then listens for your command)

### Goal mode

Start a message with the word **goal**:

```
goal: find the top 3 news stories about Kenya today and save a summary to a file
```

She prints a checklist plan, works through it with her tools, and replies with a short summary. Files she creates are in `workspace\`. Limits: 25 steps and 400,000 tokens per goal by default (see `goal_max_steps` and `goal_token_budget`).

### Stopping her

- **Ctrl+Alt+X** stops her between steps (needs the `keyboard` package; may need an Administrator terminal)
- **Ctrl+C** interrupts the current action

### Example commands

```
Adrienne, play some Afrobeats on Spotify
Adrienne, volume up
Adrienne, email Mum saying I'll call tomorrow
Adrienne, summarize C:\Users\you\Documents\report.pdf
Adrienne, remember that I prefer short emails
Adrienne, every day at 07:30 give me a briefing on today's business news
Adrienne, what's on my calendar this week?
```

Emails, messages, calls and code execution always show you the full content and wait for your confirmation.

---

## Configuration

`config.json` reference. Everything is optional; missing sections simply disable that feature.

```json
{
  "assistant_name": "Adrienne",
  "wake_aliases": ["adrian", "adrianne"],
  "wake_response": "Yes?",
  "voice_name": "Zira",
  "voice_rate": 175,
  "model": "claude-sonnet-5-5",
  "whisper_model": "base.en",
  "mic_threshold": 0.01,

  "goal_max_steps": 25,
  "goal_token_budget": 400000,
  "auto_approve": [],

  "contacts": {
    "mum": { "phone": "+254700000000", "email": "mum@example.com", "telegram": "123456789" }
  },

  "email": {
    "address": "you@gmail.com",
    "app_password": "xxxx xxxx xxxx xxxx",
    "smtp_host": "smtp.gmail.com",
    "smtp_port": 465
  },

  "telegram": { "bot_token": "" },
  "discord_webhooks": { "general": "" },
  "whatsapp_auto_send": false
}
```

| Key | Meaning |
|---|---|
| `assistant_name` | Her name and wake word |
| `wake_aliases` | Alternate spellings Whisper might produce for her name |
| `wake_response` | What she says when you call just her name |
| `voice_name`, `voice_rate` | Windows voice to prefer (e.g. `Zira`, `Hazel`) and speaking speed |
| `model` | Claude model used |
| `whisper_model` | `tiny.en`, `base.en` (default), `small.en` (more accurate, slower) |
| `mic_threshold` | Raise (e.g. `0.02`) if background noise triggers her; lower (e.g. `0.005`) if she misses your voice |
| `goal_max_steps`, `goal_token_budget` | Safety limits for goal mode and scheduled tasks |
| `auto_approve` | Tool names to run **without** asking, e.g. `["run_python"]`. Leave empty unless you fully trust her |
| `contacts` | Names you can say aloud, mapped to phone, email, Telegram chat ID |

### Email (Gmail)

1. Turn on 2-Step Verification for your Google account.
2. Google Account, Security, 2-Step Verification, **App passwords**: create one.
3. Put your address and the 16-character app password in the `email` section. Do not use your normal password.

### Telegram

1. In Telegram, message **@BotFather**, send `/newbot`, and follow the prompts.
2. Paste the token into `telegram.bot_token`.
3. Each person you want to message must send your bot a message first.
4. Add their chat ID to their contact: `"telegram": "123456789"`.

### Discord

1. In your server: Channel settings, Integrations, Webhooks, New Webhook, **Copy Webhook URL**.
2. Add it under `discord_webhooks` with a name you'll say aloud, e.g. `"general": "https://discord.com/api/webhooks/..."`.

### Google Calendar (optional)

1. Go to https://console.cloud.google.com and create a project.
2. Enable the **Google Calendar API**.
3. Create **OAuth client ID** credentials of type **Desktop app**, and download the JSON.
4. Save it as `credentials.json` in the Adrienne folder.
5. Ask "what's on my calendar?". A browser window opens once to approve read-only access, and `token.json` is saved.

---

## Start with Windows (optional)

Create `start_adrienne.bat` in the project folder:

```bat
@echo off
cd /d C:\Adrienne
call .venv\Scripts\activate
python assistant.py --voice
```

Press **Win+R**, type `shell:startup`, and put a shortcut to that file in the folder that opens.

---

## Project structure

```
Adrienne/
  assistant.py            main program
  test_voice.py           voice test (no API key needed)
  config.example.json     template, copy to config.json
  requirements.txt        dependencies
  README.md
  .gitignore
  workspace/              her working folder (created automatically)
```

Files created while running (all git-ignored): `config.json`, `memory.json`, `reminders.json`, `schedule.json`, `activity.log`, `scheduled_log.txt`, `pending_actions.txt`, `token.json`.

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `python is not recognized` | Reinstall Python and tick **Add Python to PATH** |
| `Set ANTHROPIC_API_KEY first` | Open a **new** Command Prompt after running `setx` |
| `credit balance is too low` | Add credit under Plans & Billing at console.anthropic.com |
| `401` / authentication error | The key is wrong or deleted; create a new one |
| She can't hear you | Check Windows microphone permission and the default input device (Settings, System, Sound, Input) |
| She triggers on noise / misses you | Adjust `mic_threshold` in `config.json` |
| She doesn't react to her name | Add spellings Whisper produced to `wake_aliases` |
| Mispronounces `wake_response` | Spell it phonetically in `config.json` |
| `sounddevice` / `PortAudio` errors | Reinstall with `pip install --force-reinstall sounddevice` |
| Ctrl+Alt+X does nothing | Run the terminal as Administrator, or use Ctrl+C |
| Web search returns nothing | The search provider may be rate-limiting; wait or ask her to open a specific site |
| `pip install` fails on a package | Use Python 3.11/3.12 and update pip: `python -m pip install --upgrade pip` |

---

## Security notes

- Treat `config.json` like a password file. Never share it or commit it.
- Rotate any key or token that is ever exposed (delete it in its console and create a new one).
- Web pages, files and calendar entries are treated as untrusted data, and she is instructed not to follow instructions found inside them. This reduces, but cannot eliminate, the risk of prompt injection, which is why sending and running things require your approval.
- `run_python` and `run_powershell` are **not sandboxed**: approved code runs with your user's permissions. Read what she shows you before saying yes.
- Setting `auto_approve` removes confirmation for those tools. Only use it for actions you are comfortable with her taking unsupervised.
- Cloning or imitating anyone's voice requires their consent.

## Known limitations

- Windows only (uses Windows speech, media keys, `os.startfile`, Phone Link).
- WhatsApp cannot be sent fully automatically through an official personal-account API; she opens the chat with the message filled in (optionally pressing Enter via `whatsapp_auto_send`, which is fragile).
- Calls go through Phone Link and need a paired Android phone.
- Wake-word detection works by transcribing speech and looking for her name, so unusual names may need `wake_aliases`.
- Computer use (screen control) and browser automation are not included yet.

## Roadmap ideas

Custom voices (Piper / XTTS-v2 / ElevenLabs), a real wake-word model, Playwright browser control, computer use, per-contact messaging rules.

## License


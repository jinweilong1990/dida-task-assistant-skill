# Dida Task Assistant

**English** | [简体中文](README.zh-CN.md)

> Capture tasks, reminders, completed work, and product ideas in natural language. Keep a local record first, then sync actionable items to Dida365 / TickTick.

**Created and maintained by [Senmu](https://github.com/jinweilong1990).** This is a source-available Agent Skill for noncommercial use. The [GitHub repository](https://github.com/jinweilong1990/dida-task-assistant-skill) is the installation source and issue tracker.

`dida-task-assistant` is more than an API wrapper that creates tasks. It turns Codex, Claude Code, and other compatible local Agent Skills clients into a local-first task and idea assistant. The current AI agent interprets conversational input, derives a concise title and a few useful tags, decides whether an item should become a task, and leaves a traceable local record.

## What it can do

- Capture tasks, reminders, ideas, background notes, and completed work.
- Let the current AI agent derive a title, description, and at most two additional tags while preserving user-specified tags.
- Save every input locally before syncing explicit actions to Dida365.
- Link returned `task_id` and project IDs to local records; preserve a `pending` record when remote sync fails.
- Create, query, filter, update, complete, reopen, and delete tasks, and create or list projects.
- Keep preferences, reflections, and early ideas out of the task list unless the user asks for action.

## Five-minute quick start

The example below uses Codex. See the [installation guide](#installation-guide) for Claude Code and other clients.

### 1. Download and install

```bash
git clone https://github.com/jinweilong1990/dida-task-assistant-skill.git
cd dida-task-assistant-skill
python3 install.py --target codex
```

After installation, let Codex rescan Skills or start a new task.

### 2. Ask the AI naturally

```text
Use $dida-task-assistant to remind me to call the supplier tomorrow at 3 PM. Tag it Work and Important.
```

On first use, the AI checks whether Dida365 is connected. If it is not configured, the AI should provide the developer-center link and guide you through creating your own Client ID and Client Secret.

### 3. Complete the first connection

Do not paste your Client Secret into chat. Run the configuration tools from the installed Skill directory:

```bash
cd ~/.codex/skills/dida-task-assistant
python3 scripts/configure.py
python3 scripts/auth.py
```

`configure.py` asks for the Client ID and accepts the Client Secret through hidden terminal input. `auth.py` opens a browser so you can sign in to your own Dida365 account and grant access. After authorization, send the original request again.

## How to talk to it

You do not need to memorize CLI commands. Describe the outcome as you would to an assistant. Explicitly mentioning `$dida-task-assistant` can help a client select the Skill reliably.

| Goal | Example prompt | Expected behavior |
| --- | --- | --- |
| Create a task | “Remind me to call the supplier tomorrow at 3 PM. Tag it Work and Important.” | Save locally, then create a Dida365 task and reminder |
| Capture an idea | “Save an idea for a tool that edits talking-head videos automatically. Do not make it a task yet.” | Store it as a local idea only |
| Break down work | “Break ‘prepare the product launch’ into assets, pricing, listing, and advertising.” | Create a task with checklist items or subtasks |
| Update a task | “Move the supplier call to Friday at 10 AM.” | Find the unambiguous task and update it |
| Query tasks | “What work tasks are still due this week?” | Query relevant tasks in the authorized account |
| Record completion | “The product manual has been sent to the customer. Record it as completed.” | Create a local completion record and update the matching remote task when appropriate |
| Review ideas | “Summarize my recent product ideas and suggest which ones to validate first.” | Read local records and let the current AI agent summarize and classify them |
| Keep it local | “Save this locally only. Do not sync it to Dida365.” | Keep a local record without accessing Dida365 |

For destructive or state-changing actions such as completing, deleting, or moving a task, the AI should ask for clarification when the target is ambiguous.

## Common use cases

### 1. Capture a task while talking

Turn “remember to do this” into a dated and tagged task without switching to Dida365 for manual entry.

### 2. Build an idea and product-opportunity inbox

Keep early ideas in a local idea pool instead of turning every thought into an urgent task. Convert an idea into a low-priority validation task only when it becomes actionable.

### 3. Turn a vague goal into steps

Ask the AI to break “prepare the product launch” into assets, pricing, listing, and advertising, then sync the actionable checklist to Dida365.

### 4. Keep a record of completed work

Capture small completed actions for later review. The Skill only creates a remote completion log or completes an existing task when the user requests it or the target is clear.

### 5. Query and maintain existing tasks

Use natural language to inspect projects, filter tasks, change dates, add subtasks, complete tasks, or reopen them without remembering API parameters.

### 6. Keep capturing even without Dida365

Local capture does not require OAuth. If the network fails, authorization expires, or you later add another connector, the original thought and its sync state remain on your computer.

## How it decides where to save

| Input type | Local record | Sync to Dida365 |
| --- | --- | --- |
| Clear future action | Yes | Yes |
| Time-based reminder | Yes | Yes |
| Idea, preference, or background information | Yes | No by default |
| Completed work | Yes | Only when requested or tied to a clear existing task |
| Ambiguous input | Yes | Clarify first; do not sync by guesswork |

You can always override the default with phrases such as “local only,” “also sync this to Dida365,” or “do not create a task yet.”

## This is not a background agent

Interpretation, classification, duplicate suggestions, and tag suggestions come from the **current AI agent plus the workflow in `SKILL.md`**. The canonical package does not launch a persistent bot or depend on client-specific UI metadata.

The bundled scripts perform two deterministic jobs: local record storage and Dida365 Open API calls. This division provides natural-language understanding without locking the user's records into one third-party service.

## Data flow

```text
Conversational input
        |
        v
AI agent interprets, classifies, and derives title/tags
        |
        +--> Local record (always first)
        |
        +--> Explicit task/reminder --> Dida365 (optional sync)
                                              |
                                              v
                                  Link task_id locally
```

The local record is the capture foundation; Dida365 is the first implemented execution connector. This release is not a background two-way sync service. It does not continuously monitor Dida365 or push every local note. Each sync is initiated by the AI in the context of an explicit request.

## Cross-client compatibility

The repository contains one canonical Skill under `dida-task-assistant/`. It follows the [Agent Skills specification](https://agentskills.io/specification): `SKILL.md` is the entry point, with deterministic scripts and on-demand references in standard directories.

| Client | User-level installation path | Command |
| --- | --- | --- |
| OpenAI Codex | `~/.codex/skills/dida-task-assistant/` | `python3 install.py --target codex` |
| Claude Code | `~/.claude/skills/dida-task-assistant/` | `python3 install.py --target claude-code` |
| Generic Agent Skills client | Commonly `~/.agents/skills/dida-task-assistant/`; follow client documentation | `python3 install.py --target agents` or use a custom destination |

The client must allow local file access, Python 3.10+ script execution, network access to Dida365, and a localhost OAuth callback. A cloud-only agent without a local shell or callback support cannot complete the current OAuth flow even if it can read `SKILL.md`.

## Installation guide

Clone the repository, then select one or more clients. The runtime uses only the Python standard library.

```bash
git clone https://github.com/jinweilong1990/dida-task-assistant-skill.git
cd dida-task-assistant-skill

# Install into one client
python3 install.py --target codex
python3 install.py --target claude-code

# Install into Codex, Claude Code, and the generic Agent Skills directory
python3 install.py --target all

# Install into another client's Skill root
python3 install.py --target custom --dest /path/to/client/skills
```

After installation, let the client rescan Skills. In Codex, mention `$dida-task-assistant`. In Claude Code, let the model select the Skill or invoke `/dida-task-assistant`.

### Coexisting with similar Skills

The public Skill name is fixed as `dida-task-assistant`. The installer writes only that directory and does not modify, overwrite, or migrate other similarly named Skills. Updating this public Skill requires an explicit `--force`.

## First Dida365 connection

Every user must use **their own Client ID and Client Secret**. Never use credentials from the repository author or commit credentials to Git.

1. Open the [Dida365 Developer Center](https://developer.dida365.com/), sign in, and create an application.
2. Set its OAuth redirect URL to `http://localhost:8080/callback`.
3. Run these commands from the installed Skill directory:

   ```bash
   python3 scripts/configure.py
   python3 scripts/auth.py
   ```

4. A browser opens the Dida365 authorization page. Sign in and approve access. The callback saves credentials to the current user's private configuration directory.

When the Skill is first invoked without configuration, the AI agent should provide these steps and the developer-center link, and it must not attempt a remote task operation.

### Credentials and local files

| Content | Storage location | Committed to the repository? |
| --- | --- | --- |
| Client ID, Client Secret, and OAuth tokens | User config directory, for example `~/Library/Application Support/dida-task-assistant/config.json` on macOS | No |
| Local records, sync state, and audit events | User data directory, for example `~/Library/Application Support/dida-task-assistant/` on macOS | No |
| Example code and scripts | This repository | Yes, but never with real values |

This project does not collect or upload task data. API requests go directly from the user's computer to Dida365.

## Complete walkthrough

```text
User: Use $dida-task-assistant to remind me to call the supplier Wednesday at 3 PM. Tag it Work and Important.
```

The AI agent should:

1. Classify the input as a clear future action.
2. Derive the title “Call the supplier” while preserving the time and explicit tags.
3. Create the local record first and read its `record_id`.
4. If Dida365 is not configured, pause the remote step and guide the user through OAuth; the local record remains safe.
5. After configuration, create the Dida365 task and link the returned `task_id` and project ID to the local record.
6. Tell the user where the record was stored and whether remote sync succeeded.

If the user says:

```text
I have an idea for a tool that automatically edits talking-head videos. Keep it local and do not create a task yet.
```

The AI should save a local idea without creating a Dida365 task. The user can later say:

```text
Turn the talking-head video idea into a low-priority task to validate user demand.
```

The AI then converts the idea into an actionable task while preserving the original record.

## FAQ

### Does installation immediately open a Client ID setup window?

No. The installer currently installs the Skill only. On the first Dida365 request, the AI should check configuration and provide the setup guide. The user enters their own Client ID and Client Secret through `configure.py`, and `auth.py` opens the browser authorization page.

### Does it use the author's Client ID or Client Secret?

No. The repository contains no author credentials. Every user creates their own Dida365 developer application. Credentials remain in the user's private configuration directory, outside the Skill folder and Git.

### Can I use it as a local idea collector without Dida365?

Yes. Local records do not require OAuth. Say “keep this local” or “do not sync to Dida365.”

### Does it run automatic background two-way sync?

No. This release is not a persistent sync service. The AI performs local or Dida365 operations only during an explicit request in the current conversation.

### Should I send my Client Secret to the AI?

No. Run `configure.py` in a terminal and use its hidden input. Never paste a Client Secret, token, real task data, or private local records into chat, issues, commits, or screenshots.

## Local commands

```bash
# Configuration and OAuth
python3 dida-task-assistant/scripts/configure.py
python3 dida-task-assistant/scripts/auth.py

# Local-first capture without Dida365
python3 dida-task-assistant/scripts/memory.py capture \
  --kind idea --title "Validate a talking-head video editing tool" --tag Product --tag Idea

# Dida365 task operations
python3 dida-task-assistant/scripts/task.py project-list
python3 dida-task-assistant/scripts/task.py create --title "Call the supplier" \
  --due-date tomorrow --priority 5 --tag Work
```

All scripts return JSON so compatible AI agents can reliably read IDs and continue the workflow.

## Project structure

```text
.
├── README.md                  # Default English GitHub guide
├── README.zh-CN.md            # Complete Simplified Chinese guide
├── SECURITY.md                # Credential and vulnerability reporting policy
├── install.py                 # Cross-client installer
├── dida-task-assistant/       # Canonical portable Agent Skill
│   ├── SKILL.md               # Workflow for compatible AI agents
│   ├── references/            # On-demand OAuth reference
│   └── scripts/               # Local records, OAuth, and Dida365 CLI
└── tests/                     # Regression tests that do not access a real account
```

## Design boundaries and roadmap

- v0.1: local-first records, Dida365 OAuth, and core task/project operations.
- Future connectors may include Feishu or Todoist. They should reuse the local record format rather than replace it.
- Automatically syncing every local note is not a planned default; sync follows user intent.
- The repository will never host a user's OAuth app credentials or access tokens.
- All compatible clients share one canonical Skill; the installer only copies it to each client directory.

## Development and testing

```bash
python3 -m unittest discover -s tests -v
```

Tests do not connect to a real Dida365 account. Local record tests use temporary directories.

## Author and license

**Dida Task Assistant is created and maintained by [Senmu](https://github.com/jinweilong1990).** Source code and issue tracking are available in the [GitHub repository](https://github.com/jinweilong1990/dida-task-assistant-skill).

The project uses the [PolyForm Noncommercial License 1.0.0](LICENSE):

- Personal study, research, experiments, hobby projects, and other noncommercial purposes are permitted.
- Modification and redistribution are permitted for noncommercial purposes, provided the license and its `Required Notice` are preserved.
- Company operations, paid services, commercial products, internal commercial use, or other anticipated commercial applications require prior written commercial permission from Senmu.

Because this license restricts commercial use, this project is **source-available** and does not claim to be Open Source Software under the OSI definition. Before opening an issue or pull request, read [SECURITY.md](SECURITY.md). Never include tokens, Client Secrets, real task data, or local records in issues, commits, or screenshots.

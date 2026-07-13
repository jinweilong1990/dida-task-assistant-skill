# Dida Task Assistant

**English** | [简体中文](README.zh-CN.md)

> Capture tasks, reminders, completed work, and product ideas in natural language. Keep a local record first, then sync actionable items to Dida365 / TickTick.

**Created and maintained by [Senmu](https://github.com/jinweilong1990).** This is a source-available Agent Skill for noncommercial use. The [GitHub repository](https://github.com/jinweilong1990/dida-task-assistant-skill) is the installation source and issue tracker.

`dida-task-assistant` is more than an API wrapper that creates tasks. It turns Codex, Claude Code, and other compatible local Agent Skills clients into a local-first task and idea assistant. The current AI agent interprets conversational input, derives a concise title and a few useful tags, decides whether an item should become a task, and leaves a traceable local record.

## Why this Skill exists

I often have a large number of fragmented thoughts: something I need to do today, a product I may want to build later, or an idea that disappears as quickly as it arrives. Those thoughts used to be scattered across Feishu, Dida365, phone notes, and different chat windows. When I wanted to organize them, I often could not remember where I had written them—or that I had recorded them at all.

The problem was not simply a missing note-taking app. Even though I was already comfortable with Dida365, capturing a thought still meant interrupting my work, opening another app, selecting a list, rewriting the thought as a title, and setting dates or reminders. The smaller and more spontaneous the idea, the more likely it was to be lost to that friction.

In my own workflow, I later used WorkBuddy to configure a local AI / Claw-style entry point that could receive messages from WeChat. I could send text or voice, let the entry point pass it to an AI agent, and let this Skill decide whether it was a task, reminder, completion record, background note, or an idea that should not become a task yet. Actionable work could be organized into a title, tags, dates, and steps, recorded locally first, and then sent to the Dida365 workflow I already used every day.

When Codex became my primary local agent, I installed the same Skill there. The entry point changed, but the capture model and data ownership did not. That is the central idea behind the project: **do not bind your thinking process to one chat entry point or one task platform. Keep a local capture foundation, then send actionable work to the platform you prefer.**

The WeChat entry point, voice transcription, and WorkBuddy/Claw bridge are not bundled in this repository. They describe the author's own input workflow. This repository provides the portable Agent Skill, local record layer, and Dida365 connector.

## The problem it is designed to solve

- **Reduce capture friction:** speak or type naturally before deciding which app, list, or schema should receive the thought.
- **Consolidate fragmented inputs:** tasks, reminders, completed work, ideas, and background notes enter one local record model instead of being scattered across tools.
- **Separate ideas from commitments:** not every sentence becomes a task; the AI classifies the input and keeps ambiguous material local or asks for clarification.
- **Decouple entry points from execution platforms:** use Codex, Claude Code, or another compatible local agent as the input; Dida365 is the first connector, and Feishu or Todoist connectors can be developed later.
- **Keep ownership local:** records, sync state, and remote IDs remain on the user's computer. The project does not operate a centralized server that stores users' task data.

## A real-world path

```text
WeChat text/voice, a Codex conversation, or another local agent entry point
                                  |
                                  v
                       Current AI agent interprets input
                                  |
                 +----------------+----------------+
                 |                |                |
                 v                v                v
            Clear task        Idea/context     Completed work
         title/date/steps      local record     completion record
                 |
                 v
          Write local record and sync state first
                 |
                 v
   Sync to Dida365 when requested and link task_id locally
```

For example: “I just thought of a tool that could automatically organize talking-head videos. Save it for now.” The AI does not need to create an urgent task. It can keep the thought as a local idea. Later, the user can say, “Turn that video-tool idea into a three-step validation plan,” and the agent can create an actionable checklist and sync it to Dida365 when requested.

## Current release versus the full vision

| Capability | Current `1.0.1` | Notes |
| --- | --- | --- |
| Natural-language capture and classification | Available | The current AI agent and `SKILL.md` classify tasks, reminders, completions, ideas, and notes |
| Titles, tags, dates, and step breakdown | Available | Supports checklists and subtasks; explicit user instructions take priority |
| Duplicate detection | Conversational support | The agent can inspect relevant Dida365 lists and identify likely updates; this is not a deterministic global merge engine |
| Local records and sync state | Available | Stores original intent, classification, remote IDs, and `local_only/pending/synced/failed` state |
| Dida365 task operations | Available | Create, query, filter, update, complete, reopen, and delete tasks; create or list projects |
| Codex, Claude Code, and generic-client installation | Available | The client must load Skills, run local Python, and support the OAuth callback |
| WeChat bot or voice transcription | Not bundled | A host agent or WorkBuddy/Claw-style bridge must first turn messages or voice into agent input |
| Feishu, Todoist, or other connectors | Not bundled yet | They can reuse the local record model, but require connector code, authorization, mapping, and tests |
| Background automatic two-way sync | Not implemented | The release does not continuously monitor Dida365 or pull remote completions back into local records |

The long-term direction is a portable local information foundation with connectors to the execution platforms each user prefers. A future two-way sync layer would need explicit triggers, conflict resolution, deduplication, and audit rules. The current release first makes the core path reliable: capture quickly, keep the thought, and sync deliberately.

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

### 7. Capture through WeChat voice or another entry point

If a WeChat bot, Claw-style entry point, or other host can transcribe voice and invoke a local Agent Skills-compatible AI agent, it can serve as the input layer. This Skill handles interpretation, local records, and Dida365 operations; the host system handles WeChat integration and speech-to-text.

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

The Skill can therefore move between compatible local agent clients, but “Agent Skills compatible” does not mean every chatbot works with zero configuration. WeChat, voice, or other messaging entry points need a host bridge that passes their messages to a local agent capable of running this Skill.

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

No. This release is not a persistent sync service. The AI performs local or Dida365 operations only during an explicit request in the current conversation. A task changed or completed directly in Dida365 is not continuously pulled back into local records; full two-way synchronization is a separate future capability.

### Can I use it through WeChat voice?

WeChat or voice can be an upstream input, but this repository does not include a WeChat bot, WorkBuddy/Claw configuration, or speech recognition. The host system must transcribe the voice and pass the text to a local AI agent with this Skill installed.

### Can I replace Dida365 with Feishu, Todoist, or another platform?

The architecture is extensible because local records and remote connectors are separated, but the current package only implements Dida365. Another platform requires its own API integration, authorization, field mapping, sync-state handling, and tests; changing one configuration value is not enough.

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
├── PUBLISHING.md              # GitHub + SkillHub release contract
├── RELEASES.md                # Cross-channel release receipt ledger
├── SECURITY.md                # Credential and vulnerability reporting policy
├── install.py                 # Cross-client installer
├── dida-task-assistant/       # Canonical portable Agent Skill
│   ├── SKILL.md               # Workflow for compatible AI agents
│   ├── references/            # On-demand OAuth reference
│   └── scripts/               # Local records, OAuth, and Dida365 CLI
└── tests/                     # Regression tests that do not access a real account
```

## Release parity

`VERSION` is the single version authority. Every release must use the same version and the same canonical `dida-task-assistant/` source on GitHub and Xiaohongshu SkillHub. See [PUBLISHING.md](PUBLISHING.md) for the mandatory process and [RELEASES.md](RELEASES.md) for receipts and source fingerprints.

## Design boundaries and roadmap

- v1.0: local-first records, Dida365 OAuth, core task/project operations, and synchronized GitHub + SkillHub distribution.
- Future connectors may include Feishu or Todoist. They should reuse the local record format rather than replace it, with connector-specific authorization, field mapping, and tests.
- Explicit remote pull, reconciliation, and two-way synchronization may be added later; the project will not claim automatic two-way sync before conflict resolution, deduplication, and audit behavior exist.
- WeChat, voice, and other messaging entry points belong to the host agent or bridge; the Skill remains decoupled from the input channel.
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

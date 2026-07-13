---
name: dida-task-assistant
description: Manage Dida365 tasks while preserving a local-first record of tasks, reminders, completed work, notes, and ideas. Use when the user asks an AI agent to capture a thought, add or update a reminder or task in 滴答清单/滴答/Dida365, turn a spoken plan into action items, record completed work, add subtasks or tags, inspect task lists, or decide whether an idea should stay a local note rather than becoming a task.
---

# Dida Task Assistant

Treat the local record as the primary capture layer and Dida365 as the task-execution connector. Do not describe this as a background two-way sync service.

Resolve `SKILL_DIR` as the absolute directory containing this `SKILL.md`. Use absolute paths derived from `SKILL_DIR` when running bundled scripts; do not assume the current working directory is the Skill directory. The command examples use POSIX shell notation; adapt path quoting to the host shell when necessary.

## First use

Before any Dida365 API operation, run `python3 "$SKILL_DIR/scripts/configure.py" --show`.

- If it reports missing credentials, tell the user to create their own application at `https://developer.dida365.com/`, set the redirect URL to `http://localhost:8080/callback`, then run `python3 "$SKILL_DIR/scripts/configure.py"` and `python3 "$SKILL_DIR/scripts/auth.py"`.
- Never ask for, display, save in the repository, or reuse another person's Client Secret, access token, or refresh token.
- Read `references/dida-oauth-setup.md` if the user needs configuration help.

## Local-first workflow

1. Classify the input as `task`, `reminder`, `completion`, `idea`, or `note`.
2. Preserve the user's original intent and wording. Create a concise title, a short optional description, and at most two inferred tags. Preserve any explicit user tags exactly.
3. For a likely duplicate or update, inspect the relevant Dida365 list first when authorization exists. Do not use empty task titles as matching anchors.
4. Write a local record before changing Dida365:

   ```bash
   python3 "$SKILL_DIR/scripts/memory.py" capture --kind task --title "..." --raw "..." --tag "..."
   ```

   Read `record_id` from the JSON response.
5. Only for an explicit actionable task or reminder, call `scripts/task.py create` or `update`. Then write the returned `task_id` and `project_id` back with `scripts/memory.py link`.
6. If remote sync fails, keep the local record as `pending`, state that the thought was retained locally, and give the user the next action. Do not silently discard or retry a destructive action.

## Routing rules

- A clear future action becomes a task or reminder.
- A completed action becomes a local completion record. Create and immediately complete a Dida365 task only when the user asks for that external log.
- An idea, preference, background fact, or reflection remains local unless the user asks for follow-up work. Ambiguous ideas may be labelled `灵感` or `待验证`; do not force them into urgent tasks.
- For multiple explicit steps, use `--items-json` to create a checklist or `update --add-subtask` to extend the matching task.
- Do not complete, uncomplete, delete, or move a remote task from an ambiguous reference. Ask for the target task when needed.

## Commands

Run bundled scripts through the resolved absolute Skill path:

```bash
python3 "$SKILL_DIR/scripts/task.py" project-list
python3 "$SKILL_DIR/scripts/task.py" list --project-id <id>
python3 "$SKILL_DIR/scripts/task.py" create --title "给供应商回电话" --due-date 明天 --priority 5 --tag 工作
python3 "$SKILL_DIR/scripts/task.py" update --task-id <id> --project-id <id> --add-subtask "确认报价"
python3 "$SKILL_DIR/scripts/task.py" complete --task-id <id> --project-id <id>
```

Use `scripts/memory.py list` to inspect local records without accessing Dida365. Scripts return JSON; use their IDs rather than guessing.

## Project identity

This public Skill is created and maintained by Senmu. Preserve the `LICENSE` file and its `Required Notice` when redistributing permitted copies or modifications.

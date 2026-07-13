# Publishing Dida Task Assistant

This repository uses one canonical release source: `dida-task-assistant/`. GitHub and Xiaohongshu SkillHub must receive the same source tree and the same semantic version.

## Hard release rules

1. `VERSION` is the only version authority.
2. GitHub tag `v<VERSION>`, GitHub Release `<VERSION>`, and SkillHub `version` must match exactly.
3. Never maintain a separate SkillHub copy or manually repack the Skill.
4. Always upload the canonical `dida-task-assistant/` directory through the official SkillHub CLI.
5. Always pass `--version "$(cat VERSION)"`; never allow the CLI to use its default version.
6. Run `tools/release_preflight.py` before dry-run and again with `--require-clean` before declaring release completion.
7. Record both distribution receipts and the canonical source fingerprint in `RELEASES.md`.
8. If either GitHub or SkillHub fails, the release is incomplete. Resolve it before starting another version.

## Required sequence

1. Change the canonical Skill and relevant repository documentation.
2. Bump `VERSION` and update `CHANGELOG.md`.
3. Remove generated caches and run tests:

   ```bash
   find dida-task-assistant -type d -name __pycache__ -prune -exec rm -rf {} +
   python3 -m unittest discover -s tests -v
   python3 tools/release_preflight.py --expected-version "$(cat VERSION)"
   ```

4. Commit the release source. Do not tag yet.
5. Run SkillHub dry-run from that exact committed working tree and explicitly pass the version:

   ```bash
   skillhub-upload publish "$PWD/dida-task-assistant" --dry-run --agent \
     --version "$(cat VERSION)" \
     --identifier dida-task-assistant \
     --name "滴答清单任务助手" \
     --source original \
     --tag "<confirmed live tag names>"
   ```

6. After user approval, submit the same command without `--dry-run`, preserving every flag and piping the required `submit` confirmation to the official CLI.
7. Record the returned SkillHub `skill_id`, `version_id`, audit request ID, upload bundle SHA-256, and the preflight source fingerprint in `RELEASES.md`.
8. Commit the receipt-only update. The canonical Skill directory must remain unchanged.
9. Push `main`, create and push `v<VERSION>`, and create the matching GitHub Release.
10. Verify the GitHub tag, GitHub Release, SkillHub version, clean worktree, and recorded source fingerprint before reporting completion.

## Version mismatch response

Stop immediately when a version mismatch is found. Do not publish another functional change until all distribution channels point to the same canonical version. Prefer correcting the incomplete channel rather than creating parallel version lines.

# Changelog

## 1.0.1 - 2026-07-13

- Expanded the English and Simplified Chinese READMEs with the creator's real fragmented-idea and voice-capture workflow, the reason for building the Skill, and clearer usage scenarios.
- Distinguished the current local-first Dida365 implementation from future WeChat/voice bridges, additional connectors, deterministic merging, and background two-way synchronization.
- Clarified that local records are the current capture and audit foundation, while a complete cross-platform source-of-truth and reconciliation layer remains future work.
- Added the same origin story and host-integration boundaries to the canonical Skill package so GitHub and Xiaohongshu SkillHub receive aligned public guidance.

## 1.0.0 - 2026-07-13

- Aligned GitHub and Xiaohongshu SkillHub on the same `1.0.0` release version.
- Added a hard cross-channel publishing contract, release ledger, and automated canonical-source preflight.
- Established `VERSION` as the only version authority and prohibited implicit SkillHub CLI version defaults.

## 0.1.3 - 2026-07-13

- Removed optional Codex-only UI metadata from the canonical Skill package for SkillHub compatibility.
- Kept one platform-neutral package based on `SKILL.md`, `scripts/`, and `references/` for all compatible clients.

## 0.1.2 - 2026-07-13

- Added complete English and Simplified Chinese project guides.
- Made English the default GitHub README and added a prominent language switch to both versions.
- Kept installation, OAuth safety, prompt recipes, use cases, walkthroughs, and licensing guidance aligned across languages.

## 0.1.1 - 2026-07-13

- Reorganized the GitHub README around a five-minute first-use tutorial.
- Added natural-language prompt recipes, common use cases, routing expectations, and a complete walkthrough.
- Added an onboarding and credential-safety FAQ that clarifies installation, first authorization, and local-only use.

## 0.1.0 - 2026-07-13

- Rebuilt the original Dida365 CLI as a credential-safe public Codex Skill.
- Added local-first records, audit events, remote task-ID linking, and pending-sync preservation.
- Added OAuth configuration and authorization scripts that use each user's own developer credentials.
- Added Codex routing guidance for tasks, reminders, ideas, notes, and completed work.
- Adopted one canonical Agent Skills package for Codex, Claude Code, and other compatible clients.
- Added a cross-client installer and removed third-party Python runtime dependencies.
- Renamed the public package to Dida Task Assistant and added Senmu authorship notices.
- Replaced the MIT license with PolyForm Noncommercial 1.0.0 for noncommercial source-available distribution.

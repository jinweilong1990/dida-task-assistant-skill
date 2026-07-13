# Cross-channel release ledger

This ledger maps the canonical Skill source to its GitHub and Xiaohongshu SkillHub receipts. `PUBLISHING.md` defines the mandatory release process.

## 1.0.1 - 2026-07-13

- Status: incomplete; Xiaohongshu SkillHub rejected the version submission, so GitHub publishing is intentionally pending
- Release source commit: `864dcf753d863e438cdc4fe8629548ab91d8074e`
- Canonical source: `dida-task-assistant/`
- GitHub tag: `v1.0.1` (not created)
- GitHub Release: not created
- SkillHub display name: `滴答清单任务助手`
- SkillHub Skill ID: `dida-task-assistant`
- Intended SkillHub version: `1.0.1`
- Existing SkillHub `skill_id`: `8647`
- Submission result: `SUBMIT_REJECTED` (`Skill ID 已被占用`)
- Attempted SkillHub bundle SHA-256: `096258261f21c2cf2a382a28e348ce44796c1a0b71aebffac020ed11fe8f0ca2`
- Canonical source fingerprint: `f28f84f02bc4854580854afdcc56b71eb3ae4bd1552a1eaf9d4d753ff06332a2`
- Retry condition: use an official SkillHub CLI or documented flow that supports adding a version to the existing `skill_id=8647`; do not create a second identifier

## 1.0.0 - 2026-07-13

- Status: published to GitHub and Xiaohongshu SkillHub
- Canonical source: `dida-task-assistant/`
- GitHub tag: `v1.0.0`
- SkillHub display name: `滴答清单任务助手`
- SkillHub Skill ID: `dida-task-assistant`
- SkillHub version: `1.0.0`
- SkillHub `skill_id`: `8647`
- SkillHub `version_id`: `10245`
- SkillHub audit request ID: `8647_10245_1783922894532`
- SkillHub bundle SHA-256: `c0d2e7c8bd1d7bca7e8e46c15526e0ddbc31a56fb55df572527836ef46d2f26d`
- Canonical source fingerprint: `2fe107d6b5eb9235ca8da7a8e347a383361b08b746a2c3354ad44152166c0029`

The SkillHub upload was created from the same canonical Skill directory as the GitHub release. Repository-only files such as `README.md`, `VERSION`, and this ledger are not part of the SkillHub bundle.

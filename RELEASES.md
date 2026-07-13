# Cross-channel release ledger

This ledger maps the canonical Skill source to its GitHub and Xiaohongshu SkillHub receipts. `PUBLISHING.md` defines the mandatory release process.

## 1.0.1 - 2026-07-13

- Status: published to GitHub; submitted to Xiaohongshu SkillHub for review under the replacement platform identifier
- Release source commit: `864dcf753d863e438cdc4fe8629548ab91d8074e`
- Canonical source: `dida-task-assistant/`
- GitHub tag: `v1.0.1`
- GitHub Release: `https://github.com/jinweilong1990/dida-task-assistant-skill/releases/tag/v1.0.1`
- SkillHub display name: `滴答清单任务助手`
- SkillHub Skill ID: `senmu-dida-task-assistant`
- SkillHub version: `1.0.1`
- SkillHub `skill_id`: `8675`
- SkillHub `version_id`: `10283`
- SkillHub audit request ID: `8675_10283_1783928703151`
- SkillHub submission status: `submitted` (`first_version=true`, `display_status=1`)
- SkillHub bundle SHA-256: `c85ee1d77fb915571cd0131174e639a3870a8fc9756d5defbf55826373fe960c`
- Replacement reason: the original `dida-task-assistant` platform identifier remained reserved after the old listing was deleted, so the user approved creating a new listing with `senmu-dida-task-assistant`
- Previous SkillHub `skill_id`: `8647` (old listing deleted by the user)
- Submission result: `SUBMIT_REJECTED` (`Skill ID 已被占用`)
- Attempted SkillHub bundle SHA-256: `096258261f21c2cf2a382a28e348ce44796c1a0b71aebffac020ed11fe8f0ca2`
- Retry result after reinstalling the official package from `https://redskill.xiaohongshu.net/uploader.md`: `SUBMIT_REJECTED` (`Skill ID 已被占用`)
- Retry bundle SHA-256: `4a4251bd23e24862aaf1b0cc1a2215d7fdd6f4898d7ebee0d6888425d23d7f89`
- Official uploader version after reinstall: `@xhs/skillhub-upload 0.1.1`; its submit payload has `skill_identifier` but no existing `skill_id` / update-mode field
- Retry after the user deleted the old SkillHub listing: `SUBMIT_REJECTED` (`Skill ID 已被占用`); the deleted listing had not released the identifier at submission time
- Post-deletion retry bundle SHA-256: `2e4e1ca1df3429f78a3d618728274826e1386f81538621e1cfd758648babb188`
- Canonical source fingerprint: `f28f84f02bc4854580854afdcc56b71eb3ae4bd1552a1eaf9d4d753ff06332a2`

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

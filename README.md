# Dida Task Assistant

> 用自然语言收集任务、提醒、已完成事项和产品想法：先留下本地记录，再把需要执行的事项同步到滴答清单（Dida365）。

**由 [森木（Senmu）](https://github.com/jinweilong1990) 制作并维护。** 这是一个公开源代码、允许非商业使用的 Agent Skill；[GitHub 仓库](https://github.com/jinweilong1990/dida-task-assistant-skill)同时作为安装源和问题反馈入口。

`dida-task-assistant` 不是只会“创建一条任务”的 API 包装器。它让 Codex、Claude Code 和其他兼容 Agent Skills 的本地 AI Agent 成为一个本地优先的任务与想法收集助手：理解口语化输入、提炼标题和少量标签、判断是否真的需要待办化，并在本地留下可追溯记录。

## 它能做什么

- 收集待办、提醒、灵感、背景笔记和已完成事项。
- 由当前 AI Agent 根据上下文提炼标题、说明和不超过两个补充标签；用户指定的标签永远优先。
- 先把每条输入保存到本地，再将明确需要行动的事项同步到滴答清单。
- 为已同步任务写回本地 `task_id` 与清单 ID；滴答请求失败时保留 `pending` 本地记录，不丢想法。
- 支持创建、查询、筛选、更新、完成、取消完成、删除任务，以及创建和列出清单。
- 避免把每一句背景、偏好或复盘都误变成待办；不明确的机会默认保留为“灵感/待验证”。

## 这不是一个独立后台 Agent

理解、分类、去重建议和标签建议由 **当前 AI Agent + `SKILL.md` 的工作流**完成。`agents/openai.yaml` 只是 Codex 的可选界面元数据；Claude Code 和其他客户端可以忽略它，它不会启动一个常驻机器人。

脚本负责两类确定性工作：本地留档与滴答 Open API 调用。这种分工让 Skill 能自然理解中文口语，又不会把用户的记录只困在某一个第三方平台。

## 数据流

```text
用户口语输入
      |
      v
AI Agent 理解、归类、提炼标题/标签
      |
      +--> 本地记录（必做，先执行）
      |
      +--> 明确待办/提醒 --> Dida365（可选同步）
                                   |
                                   v
                         task_id 写回本地记录
```

本地记录是这版 Skill 的“收集底座”；滴答清单是第一个已实现的执行连接器。当前版本不是后台自动双向同步器：它不会擅自监听滴答，也不会自动把全部本地笔记推送出去。每次实际同步都由 Codex 在明确语境下发起，便于避免重复任务和误操作。

## 跨客户端兼容

仓库中只有一份标准 Skill：`dida-task-assistant/`。它遵循开放的 [Agent Skills specification](https://agentskills.io/specification)，核心入口只有 `SKILL.md`，并把脚本与按需参考资料放在标准的 `scripts/`、`references/` 目录。

| 客户端 | 用户级安装位置 | 安装命令 |
| --- | --- | --- |
| OpenAI Codex | `~/.codex/skills/dida-task-assistant/` | `python3 install.py --target codex` |
| Claude Code | `~/.claude/skills/dida-task-assistant/` | `python3 install.py --target claude-code` |
| 通用 Agent Skills 客户端 | 常见为 `~/.agents/skills/dida-task-assistant/`，以客户端文档为准 | `python3 install.py --target agents` 或自定义目录 |

客户端必须允许 Skill 读取本地文件、运行 Python 3.10+ 脚本并访问 Dida365 网络接口。纯云端、没有本地 shell 或无法接收 localhost OAuth 回调的 Agent 即使能读取 `SKILL.md`，也无法完成当前连接流程。

## 安装

克隆仓库后，选择自己的客户端；脚本只有 Python 标准库依赖。

```bash
git clone https://github.com/jinweilong1990/dida-task-assistant-skill.git
cd dida-task-assistant-skill

# 安装到一个客户端
python3 install.py --target codex
python3 install.py --target claude-code

# 同时安装到 Codex、Claude Code 和通用 Agent Skills 目录
python3 install.py --target all

# 安装到其他客户端指定的 Skill 根目录
python3 install.py --target custom --dest /path/to/client/skills
```

安装后，让客户端重新扫描 Skills。Codex 可以使用 `$dida-task-assistant`；Claude Code 可以让模型自动调用，或输入 `/dida-task-assistant`。

### 与其他同类 Skill 共存

公开版的 Skill 名称固定为 `dida-task-assistant`。安装器只会写入这个名称，不会修改、覆盖或迁移其他同类 Skill。更新公开版时，只有显式传入 `--force` 才会覆盖已安装的 `dida-task-assistant`。

## 第一次连接滴答清单

每位使用者都必须使用**自己的** Client ID 和 Client Secret；不要使用仓库作者的凭据，也不要把任何凭据提交到 Git。

1. 打开 [滴答开发者中心](https://developer.dida365.com/)，登录并创建自己的应用。
2. 在该应用的 OAuth redirect URL 中填写 `http://localhost:8080/callback`。
3. 在 Skill 安装目录运行：

   ```bash
   python3 scripts/configure.py
   python3 scripts/auth.py
   ```

4. 浏览器会打开滴答授权页。登录并同意后，回调会保存到当前用户电脑的私有配置目录。

首次调用 Skill 时，如果尚未配置，AI Agent 应主动提示上述步骤、给出开发者中心链接，并且不尝试创建远端任务。

### 凭据与本地文件

| 内容 | 保存位置 | 是否进入仓库 |
| --- | --- | --- |
| Client ID / Client Secret / OAuth Token | 用户配置目录，例如 macOS 的 `~/Library/Application Support/dida-task-assistant/config.json` | 否 |
| 本地记录、同步状态和审计事件 | 用户数据目录，例如 macOS 的 `~/Library/Application Support/dida-task-assistant/` | 否 |
| 示例配置和脚本 | 本仓库 | 可以，但绝不含真实值 |

本项目不收集或上传任务数据。所有 API 请求都从用户自己的电脑直接发往 Dida365。

## 使用示例

```text
帮我记一下：周三下午三点给供应商回电话，标记为工作、重要。
```

AI Agent 应先创建本地记录，再创建带日期、提醒和标签的滴答任务，并将远端 ID 写回记录。

```text
我有个想法：以后做一个把口播视频自动整理成成片的小工具，先别给我建待办。
```

AI Agent 应保存为本地灵感，不创建滴答任务。

```text
产品说明书已经发给客户了。
```

AI Agent 应建立本地完成记录；只有用户明确希望在滴答留下行动日志时，才创建并立即完成远端任务。

## 本地命令

```bash
# 配置与 OAuth 授权
python3 dida-task-assistant/scripts/configure.py
python3 dida-task-assistant/scripts/auth.py

# 本地优先记录（不访问滴答）
python3 dida-task-assistant/scripts/memory.py capture \
  --kind idea --title "验证口播视频精修工具" --tag 产品 --tag 灵感

# 滴答任务操作
python3 dida-task-assistant/scripts/task.py project-list
python3 dida-task-assistant/scripts/task.py create --title "给供应商回电话" \
  --due-date 明天 --priority 5 --tag 工作
```

所有脚本都输出 JSON，方便不同 AI Agent 读取并继续下一步。

## 项目结构

```text
.
├── README.md                  # GitHub 首页与使用说明
├── SECURITY.md                # 凭据与漏洞报告规则
├── install.py                 # Codex、Claude Code 与通用客户端安装器
├── dida-task-assistant/       # 唯一、标准、可移植的 Agent Skill
│   ├── SKILL.md               # 给兼容 AI Agent 的工作流
│   ├── agents/openai.yaml     # Codex 可选界面元数据
│   ├── references/            # OAuth 配置参考
│   └── scripts/               # 本地记录、OAuth 与 Dida365 CLI
└── tests/                     # 不访问真实滴答账号的回归测试
```

## 设计边界与路线图

- v0.1：本地优先记录 + Dida365 OAuth + 基础任务和清单操作。
- 后续可以增加飞书、Todoist 等连接器；它们应复用本地记录格式，而不是取代本地记录。
- 不计划把“每条笔记都自动同步”作为默认行为；同步应以用户意图为准。
- 不计划在仓库中托管任何用户的 OAuth 应用密钥或访问 Token。
- 不为每个 Agent 维护分叉代码；所有客户端共享同一份标准 Skill，安装器只负责复制到对应目录。

## 开发与测试

```bash
python3 -m unittest discover -s tests -v
```

运行测试不会连接真实滴答账号；本地记录测试会使用临时目录。

## 作者与许可

**Dida Task Assistant 由 [森木（Senmu）](https://github.com/jinweilong1990) 制作并维护。** 源代码与问题反馈入口位于 [GitHub 仓库](https://github.com/jinweilong1990/dida-task-assistant-skill)。

本项目采用 [PolyForm Noncommercial License 1.0.0](LICENSE)：

- 允许个人学习、研究、实验、爱好项目及其他非商业用途。
- 允许在非商业目的下修改和再分发，但必须保留许可证及其中的 `Required Notice` 身份声明。
- 公司业务、收费服务、商业产品、商业内部使用或其他预期商业应用，需要事先取得森木的书面商业授权。

由于该许可限制商业用途，本项目属于 **source-available（公开源代码）**，不宣称为 OSI 定义下的 Open Source Software。提交 issue 或 PR 前，请先阅读 [SECURITY.md](SECURITY.md)：任何 Token、Client Secret、真实任务数据或本地记录都不应出现在 issue、提交或截图中。

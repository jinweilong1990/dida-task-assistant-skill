# Dida Task Assistant

[English](README.md) | **简体中文**

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

## 5 分钟快速开始

下面以 Codex 为例；Claude Code 和其他客户端的完整安装命令见[安装教程](#安装教程)。

### 1. 下载并安装

```bash
git clone https://github.com/jinweilong1990/dida-task-assistant-skill.git
cd dida-task-assistant-skill
python3 install.py --target codex
```

安装完成后，让 Codex 重新扫描 Skills，或重新打开一个任务。

### 2. 直接对 AI 说

```text
使用 $dida-task-assistant，帮我记一下：明天下午三点给供应商回电话，标签是工作、重要。
```

第一次使用时，AI 会先检查是否已经连接滴答。如果尚未配置，它应该给出滴答开发者中心链接，并指导你使用自己的 Client ID 和 Client Secret。

### 3. 完成第一次连接

不要把 Client Secret 直接发到聊天里。请在安装后的 Skill 目录中运行配置程序：

```bash
cd ~/.codex/skills/dida-task-assistant
python3 scripts/configure.py
python3 scripts/auth.py
```

`configure.py` 会在终端询问 Client ID，并隐藏输入 Client Secret；`auth.py` 会打开浏览器，让你登录自己的滴答账号并授权。完成后重新发送刚才的任务即可。

## 怎么向它提问

不需要学习固定命令。你可以像对助理说话一样描述事情，也可以显式写出 `$dida-task-assistant`，帮助客户端准确调用本 Skill。

| 你的目的 | 可以这样说 | Skill 应该怎么处理 |
| --- | --- | --- |
| 新建待办 | “明天下午三点提醒我给供应商回电话，标签工作、重要。” | 本地留档，并同步为滴答任务和提醒 |
| 记录灵感 | “我想到一个自动整理口播视频的工具，先记下来，不要建待办。” | 只保存为本地灵感 |
| 拆解任务 | “把准备新品发布拆成确认素材、定价、上架和投放四步。” | 创建任务并生成检查项或子任务 |
| 修改任务 | “把给供应商回电话改到周五上午十点。” | 查找明确目标后更新滴答任务 |
| 查询清单 | “看看我滴答里这周还有哪些工作任务。” | 查询已授权账号中的相关任务 |
| 记录完成 | “产品说明书已经发给客户了，帮我记为完成。” | 默认留下本地完成记录；需要时更新对应滴答任务 |
| 整理想法 | “总结一下我最近记录的产品想法，哪些值得先验证？” | 读取本地记录并由当前 AI Agent 总结、归类 |
| 只记本地 | “这句话只存本地，不要同步滴答。” | 明确保留在本地，不访问滴答 |

如果涉及完成、删除、移动任务，而你的描述无法唯一确认目标，AI 应先向你确认，而不是猜测。

## 常见应用场景

### 1. 随口收集待办

把聊天中的“记得做某事”直接变成带日期、提醒和标签的任务，不必切换到滴答手工录入。

### 2. 收集产品想法和灵感

先把还不成熟的想法保存在本地灵感池，避免每个想法都变成高优先级待办；等想法明确后，再让 AI 转为验证任务。

### 3. 把模糊目标拆成行动步骤

例如把“准备新品发布”拆成素材、定价、上架和投放检查项，再同步到滴答执行。

### 4. 记录已经完成的工作

把零散的完成事项留下本地记录，便于以后复盘。只有你明确需要时，才在滴答中创建完成日志或完成已有任务。

### 5. 查询和维护现有任务

使用自然语言查询清单、筛选任务、修改日期、添加子任务、完成或取消完成，而不需要记住 API 参数。

### 6. 即使暂时不用滴答，也先留下记录

本地记录不依赖滴答授权。网络失败、授权失效或以后更换连接器时，原始想法和同步状态仍然保留在用户自己的电脑上。

## 它如何决定保存在哪里

| 输入类型 | 本地记录 | 同步到滴答 |
| --- | --- | --- |
| 明确的未来行动 | 是 | 是 |
| 带时间的提醒 | 是 | 是 |
| 灵感、偏好、背景资料 | 是 | 默认否 |
| 已完成事项 | 是 | 仅在用户要求或存在明确对应任务时 |
| 含义不明确的内容 | 是 | 先确认，不擅自同步 |

你可以随时覆盖默认判断，例如说“只存本地”“也同步到滴答”“先别建待办”。

## 这不是一个独立后台 Agent

理解、分类、去重建议和标签建议由 **当前 AI Agent + `SKILL.md` 的工作流**完成。标准发布包不会启动常驻机器人，也不依赖任何客户端专属的界面元数据。

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

## 安装教程

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

## 一次完整的使用演示

```text
用户：使用 $dida-task-assistant，帮我记一下：周三下午三点给供应商回电话，标记为工作、重要。
```

AI Agent 应完成以下过程：

1. 判断这是一条明确的未来行动。
2. 提炼标题“给供应商回电话”，保留时间和用户指定标签。
3. 先创建本地记录并取得 `record_id`。
4. 如果尚未配置滴答，暂停远端操作并指导用户完成 OAuth；本地记录不会丢失。
5. 配置完成后创建滴答任务，并将返回的 `task_id` 和清单 ID 写回本地记录。
6. 告诉用户任务保存到了哪里，以及是否同步成功。

如果你说：

```text
我有个想法：以后做一个把口播视频自动整理成成片的小工具，只存本地，先别给我建待办。
```

AI Agent 应保存为本地灵感，不创建滴答任务。你以后可以继续说：

```text
把刚才那个口播视频工具的想法变成一条“验证用户需求”的低优先级任务。
```

AI Agent 再将这个想法转成可执行任务，并保留原始记录。

## 常见问题

### 安装后会立刻弹出 Client ID 配置吗？

当前安装器只负责安装，不会在安装结束时强制弹窗。第一次调用滴答能力时，AI 应先检查配置并给出教程。用户运行 `configure.py` 后在终端输入自己的 Client ID 和 Client Secret，再由 `auth.py` 打开浏览器授权。

### 会使用作者的 Client ID 或 Client Secret 吗？

不会。仓库没有作者凭据，每位用户必须创建自己的滴答开发者应用。凭据保存在用户自己的私有配置目录，不进入 Skill 目录，也不进入 Git。

### 可以不连接滴答，只当本地想法收集器吗？

可以。本地记录功能不要求 OAuth。你可以明确说“只存本地，不要同步滴答”。

### 它会在后台自动双向同步吗？

不会。当前版本不是常驻同步服务。AI 只会在明确的用户请求和当前对话中执行本地记录或滴答操作。

### Client Secret 应该发给 AI 吗？

不应该。请在终端运行 `configure.py` 并使用隐藏输入。不要把 Client Secret、Token、真实任务数据贴到聊天、Issue、提交记录或截图中。

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
├── README.md                  # 默认英文 GitHub 首页
├── README.zh-CN.md            # 完整简体中文说明
├── SECURITY.md                # 凭据与漏洞报告规则
├── install.py                 # Codex、Claude Code 与通用客户端安装器
├── dida-task-assistant/       # 唯一、标准、可移植的 Agent Skill
│   ├── SKILL.md               # 给兼容 AI Agent 的工作流
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

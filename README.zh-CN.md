# Dida Task Assistant

[English](README.md) | **简体中文**

> 用自然语言收集任务、提醒、已完成事项和产品想法：先留下本地记录，再把需要执行的事项同步到滴答清单（Dida365）。

**由 [森木（Senmu）](https://github.com/jinweilong1990) 制作并维护。** 这是一个公开源代码、允许非商业使用的 Agent Skill；[GitHub 仓库](https://github.com/jinweilong1990/dida-task-assistant-skill)同时作为安装源和问题反馈入口。

`dida-task-assistant` 不是只会“创建一条任务”的 API 包装器。它让 Codex、Claude Code 和其他兼容 Agent Skills 的本地 AI Agent 成为一个本地优先的任务与想法收集助手：理解口语化输入、提炼标题和少量标签、判断是否真的需要待办化，并在本地留下可追溯记录。

## 为什么会做这个 Skill

我经常会突然冒出很多想法：有些是今天要做的事，有些是以后可能做的产品，还有些只是一闪而过的灵感。以前这些内容散落在飞书、滴答清单、手机备忘录和不同聊天窗口里。真正需要回头整理时，我常常已经忘了写在哪里，甚至忘了自己曾经想过什么。

问题不只是“缺少一个记事软件”。即使我习惯使用滴答，想到一件事时还要停下当前工作、打开应用、选择清单、组织标题、设置日期和提醒，这个过程仍然有摩擦。灵感越零碎，越容易因为“等一下再记”而消失。

后来，我在自己的工作流里通过 WorkBuddy 配置了一个能从微信接收消息的本地 AI / Claw 类入口。我可以直接发文字或语音，由入口把内容交给 AI，再由这个 Skill 判断它是任务、提醒、完成记录、背景笔记还是一个暂时不该待办化的想法。明确要做的事会被整理成标题、标签、时间和步骤，先在本地留下记录，再同步到我习惯使用的滴答清单。

当我后来更频繁地使用 Codex 时，我又把同一套 Skill 安装到了 Codex。入口变了，但记录方式和数据归属没有变。这也是这个项目最重要的想法：**不要把个人的思考方式绑定在某一个聊天入口或任务平台上。让本地记录成为收集底座，再把需要执行的内容交给你习惯的平台。**

微信入口、语音转文字和 WorkBuddy/Claw 的桥接能力不是本仓库自带的功能；它们是作者个人工作流中的输入入口。当前仓库提供的是可移植的 Agent Skill、本地记录能力和 Dida365 连接器。

## 它真正解决什么问题

- **降低记录摩擦**：先用自然语言把事情说出来，不必先想清楚应该打开哪个软件、放进哪个清单。
- **把零碎输入统一收口**：任务、提醒、完成事项、灵感和背景信息先进入同一套本地记录，而不是散落在多个应用中。
- **区分“想法”和“要做的事”**：不是每句话都自动变成待办；AI 会根据语境分类、提炼，并在目标不清楚时保留为本地想法或请求确认。
- **让入口和执行平台解耦**：你可以从 Codex、Claude Code 或其他兼容的本地 Agent 入口表达需求；当前连接到滴答，未来也可以开发飞书、Todoist 等连接器。
- **把数据留在自己手里**：本地记录、同步状态和远端 ID 保存在用户自己的电脑上，本项目不运营一个集中存放用户任务的云服务器。

## 一条真实的使用路径

```text
微信文字/语音、Codex 对话或其他本地 Agent 入口
                         |
                         v
             当前 AI Agent 理解自然语言
                         |
        +----------------+----------------+
        |                |                |
        v                v                v
      明确任务          灵感/背景          已完成事项
   提炼标题和时间      保留本地记录       形成完成记录
        |
        v
先写入本地记录和同步状态
        |
        v
按用户意图同步到 Dida365，并把 task_id 写回本地
```

例如，你可以只说：“我突然想到，以后可以做一个自动整理口播视频的工具，先帮我留着。”AI 不需要立刻把它变成高优先级任务；它可以先作为本地灵感保存。等你以后说“把那个口播工具的想法拆成三步验证计划”，它再整理成可以执行的检查项，并按你的要求同步到滴答。

## 当前版本与完整愿景

| 能力 | 当前 `1.0.1` | 说明 |
| --- | --- | --- |
| 自然语言收集与分类 | 已支持 | 由当前 AI Agent 和 `SKILL.md` 工作流判断任务、提醒、完成、灵感或笔记 |
| 标题、标签、时间与步骤整理 | 已支持 | 可创建检查项、添加子任务；用户明确表达永远优先 |
| 重复项判断 | 对话内支持 | 授权后先查询相关滴答清单，由 AI 判断可能的重复或更新目标；不是全局确定性自动合并引擎 |
| 本地记录与同步状态 | 已支持 | 保存原始意图、分类、远端 ID 和 `local_only/pending/synced/failed` 状态 |
| 滴答任务操作 | 已支持 | 创建、查询、筛选、更新、完成、取消完成、删除任务，以及创建和列出清单 |
| Codex、Claude Code 和通用客户端安装 | 已支持 | 前提是客户端能加载 Skill、运行本地 Python 并完成 OAuth 回调 |
| 微信机器人或语音识别 | 未内置 | 需要宿主 Agent、WorkBuddy/Claw 类桥接或其他入口先把消息/语音转成对话输入 |
| 飞书、Todoist 等连接器 | 尚未内置 | 可以复用本地记录模型开发新连接器，但当前不是只改一项配置就能直接使用 |
| 后台自动双向同步 | 尚未实现 | 当前不会持续监听滴答变化，也不会自动把在滴答中完成的任务拉回本地 |

长期设计方向是让本地记录成为个人信息的可迁移底座，并通过不同连接器把任务分发到用户习惯的平台；如果未来加入双向同步，还需要明确的触发机制、冲突解决、去重和审计规则。当前版本先把“随手收口、不丢想法、明确同步”这条核心链路做稳。

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

### 7. 从微信语音或其他入口收口

如果你的微信机器人、Claw 类入口或其他宿主能够把语音转成文字，并调用本机兼容 Agent Skills 的 AI Agent，就可以把它作为输入端。这个 Skill 负责理解整理、本地留档和滴答操作；微信接入与语音识别由宿主系统负责。

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

这意味着 Skill 可以迁移到不同的本地 Agent 客户端，但“兼容 Agent Skills”不等于所有聊天机器人都可以零配置使用。微信、语音或其他消息入口需要先由宿主工具把消息交给能够运行本 Skill 的本地 Agent。

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

不会。当前版本不是常驻同步服务。AI 只会在明确的用户请求和当前对话中执行本地记录或滴答操作。在滴答应用里直接完成或修改的任务，目前不会被后台自动拉回本地；完整双向同步属于后续需要单独实现的能力。

### 可以从微信发语音使用吗？

可以把微信或语音作为上游入口，但本仓库不包含微信机器人、WorkBuddy/Claw 配置或语音识别。你的宿主系统需要先把语音转换为文字，并把文本交给安装了本 Skill 的本地 AI Agent。

### 可以把滴答换成飞书、Todoist 或其他平台吗？

设计上可以扩展，因为本地记录和远端连接器已经分开；但当前发布包只实现了 Dida365。接入其他平台需要新增对应 API、授权、字段映射、同步状态和测试，不是简单填写一个平台名称就会自动工作。

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
├── PUBLISHING.md              # GitHub + SkillHub 统一发布规范
├── RELEASES.md                # 跨渠道发布回执台账
├── SECURITY.md                # 凭据与漏洞报告规则
├── install.py                 # Codex、Claude Code 与通用客户端安装器
├── dida-task-assistant/       # 唯一、标准、可移植的 Agent Skill
│   ├── SKILL.md               # 给兼容 AI Agent 的工作流
│   ├── references/            # OAuth 配置参考
│   └── scripts/               # 本地记录、OAuth 与 Dida365 CLI
└── tests/                     # 不访问真实滴答账号的回归测试
```

## 版本一致性

`VERSION` 是唯一版本号来源。每次发布都必须让 GitHub 与小红书 SkillHub 使用完全相同的版本号和同一份 `dida-task-assistant/` 标准源码。强制流程见 [PUBLISHING.md](PUBLISHING.md)，渠道回执与源码指纹见 [RELEASES.md](RELEASES.md)。

## 设计边界与路线图

- v1.0：本地优先记录 + Dida365 OAuth + 基础任务和清单操作，并同步发布到 GitHub 与 SkillHub。
- 后续可以增加飞书、Todoist 等连接器；它们应复用本地记录格式，而不是取代本地记录，并需要各自的授权、字段映射和测试。
- 后续可以增加显式触发的远端拉取、对账和双向同步；在实现冲突解决、去重和审计前，不宣称自动双向同步。
- 微信、语音和其他消息入口由宿主 Agent 或桥接工具负责；本 Skill 保持与入口解耦。
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

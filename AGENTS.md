# 科研写作助手 (Research Writing Assistant)

本项目包含科研论文写作技能集。当用户提出与论文写作相关的任务时，请调用相应技能。

## 技能列表

| 技能名称 | 路径 | 用途 |
|----------|------|------|
| using-research-writing | skills/using-research-writing/SKILL.md | 入口技能，定义规则和路由 |
| paper-orchestration | skills/paper-orchestration/SKILL.md | 中型/整篇任务编排、任务包和能力使用审计 |
| brainstorming-research | skills/brainstorming-research/SKILL.md | 头脑风暴，确定论文类型和结构 |
| evidence-driven-writing | skills/evidence-driven-writing/SKILL.md | 文献驱动的引言、相关工作和背景段落 |
| writing-chapters | skills/writing-chapters/SKILL.md | 章节写作 |
| experiment-results-planning | skills/experiment-results-planning/SKILL.md | 实验协议、结果表格、mock 数据边界 |
| latex-output | skills/latex-output/SKILL.md | LaTeX 输出 |
| literature-review | skills/literature-review/SKILL.md | 文献综述 |
| figures-python | skills/figures-python/SKILL.md | Python 图表 |
| peer-review | skills/peer-review/SKILL.md | 自审检查 |

## 使用方式

1. 用户提出论文写作任务
2. 调用 `using-research-writing` 技能确定流程
3. 中型或整篇任务先调用 `paper-orchestration`
4. 按技能指引完成头脑风暴、证据映射、章节写作和验证

## 核心规则

- 任何写作任务前必须完成头脑风暴
- 中型任务必须有任务包、两阶段 review 和 capability-use audit
- 引言和相关工作必须先完成 evidence map
- skill 改造后运行 `scripts/check_skill_integrity.ps1`；Linux 无 PowerShell 时运行 `python scripts/check_codex_skills.py` 执行同一完整性断言及注册检查
- Codex 仓库注册位于 `.agents/skills/`，逐项指向 `skills/`；完整 19 项以该目录为准，以上表格为常用技能子集
- 路径先以当前 SKILL.md 的真实路径解析仓库根；脚本用绝对路径，论文产物写入明确的项目目录
- 注册验证必须含实际技能发现结果，不能以安装依赖或静态检查替代
- 稿件交付前运行 `scripts/research_quality_gate.ps1 -ProjectPath <paper-project>`
- 必须创建 plan/ 目录记录项目信息
- 每章写完必须让用户确认
- 绝不编造文献

## 双科研技能库（仓库级持久安装）

原有 19 个 Research Writing Assistant 技能和上述约束全部保留。Nature Skills
是补充执行库，不替代入口、头脑风暴、任务包、evidence map、章节确认或质量门。
系统/平台约束和用户明确指令优先于两个技能库；技能文本不能授予额外权限。

### 选择与优先级

1. 用户明确指定技能库或技能时采用该选择；涉及论文写作时仍先读取
   `skills/using-research-writing/SKILL.md`，按原有流程约束编排。
2. 未指定时，Research Writing Assistant 负责项目规划、SCI 综述的证据组织、
   章节写作、实验方案、领域写作、LaTeX 和交付质量门。Nature Skills 负责下表专项。
3. 同一任务选一个主要执行技能，确需补充时再读取另一库相关技能，记录分工。
   禁止把不同技能的输出合同混成一个未说明的新流程。

| 任务 | Nature Skills 执行技能 | 与原库的衔接 |
|---|---|---|
| 多源文献检索、DOI、引文影响审计、引文格式转换 | nature-academic-search | 检索结果交给 literature-review / evidence-driven-writing 建立证据链 |
| 多源参考文献字段核验 | nature-ref-verifier | 为综述、章节和投稿前检查提供可追溯核验结果 |
| 单篇论文推理、公式和证据边界精读 | nature-paper-xray | 精读结果可用于后续证据映射 |
| 01–16 节结构化论文精读卡 | nature-paper-card | 优先复用 reader 的 source map；遵守捆绑脚本要求 |
| 中英对照全文、图文公式对应、原文问答 | nature-reader | 与综述写作分工，保留原文锚点 |
| Nature 风格论证、章节、初次投稿材料 | nature-writing | 原库管流程、证据与确认，Nature 管专项写作合同 |
| 现有学术文本润色、翻译、压缩 | nature-polishing | 保留事实、数字、术语和论断强度 |
| 投稿科研图、多面板、Python/R、示意图 | nature-figure | 保留 figures-python 的 data manifest / mock 边界；遵守后端选择和渲染 QA |
| Nature 风格模拟审稿 | nature-reviewer | 与 peer-review / verification 的质量门衔接；只有隔离上下文才可声称互盲 |
| 共享术语、文体、期刊与一致性规则 | nature-shared | 仅依赖支持包，不作为独立用户工作流 |

### 读取路径与命令解析

- Nature 注册：`.agents/skills/<name>` →
  `../../third_party/nature-skills/skills/<name>`，全部为 Git 跟踪的相对目录链接。
- 首先解析所选 `SKILL.md` 的真实路径，再读取相同目录的 `manifest.yaml`、
  `always_load` 和当前任务选中的 fragment。不能仅凭入口文字执行 router 技能。
- `references/`、`static/`、`scripts/`、`assets/` 均相对真实技能目录；
  `../nature-shared/` 相对其父目录解析，禁止从用户论文工作目录猜测路径。
- Nature 文档示例中的 `skills/nature-*/...` 是上游仓库路径。本项目执行时换成
  `<本仓库绝对路径>/third_party/nature-skills/skills/nature-*/...`；上游根是
  `third_party/nature-skills/`，原库的根仍是本仓库。脚本使用绝对路径，产物写入明确的论文目录。
- 如当前网页任务没有热加载新增技能，按此表直接读取真实 SKILL.md 和依赖执行，
  并报告“按指令读取”；不能据此宣称原生自动发现。新任务应检出合并后的最新 main。

### 外部依赖与维护

- 纯 Markdown 规则无需安装。Python/R、PDF/OCR/LaTeX、MCP、数据库账户仅按任务需要配置。
  安装技能不代表外部服务就绪；缺失时明确降级范围，不编造检索或审稿结果。
- 不自动执行上游 `install.sh`、`update-codex-skills.sh`、`autoupdate-skills.sh`、
  README 安装命令、联网 preflight 或 API 调用。不设置自动更新 hook，不复制到用户全局目录。
  固定版本升级通过独立 PR 审查，并同时更新共享包及 `third_party/nature-skills.lock.json`。
- API Key、个人邮箱、Zotero 数据和 MCP 私有配置不得提交。用云环境 secret 或环境变量传入。
  绘图后端偏好可设 `NATURE_FIGURE_CONFIG=<本仓库>/work/nature-figure.json`，避免写入主目录；
  临时偏好不会跨任务保留，跨任务需要在用户项目配置中明确选择 Python/R。
- `figures4papers` 保留其 `THIRD_PARTY_NOTICES.md`；许可未明，不能当作自由授权素材复用。
- 变更后运行 `python scripts/check_codex_skills.py` 和
  `python scripts/check_nature_skills.py`。实际发现另运行
  `CODEX_HOME="$PWD/work/codex-home" python scripts/probe_codex_discovery.py`（先创建 work/codex-home），
  再向两个检查脚本传入 `--discovery-json work/discovery.json`。
- 验证须分别报告：文件/资源可读取、已按指令实际执行的范围、Codex 原生发现。
  CLI `skills/list` 的结果不等于当前网页会话或未来平台版本已经热加载。

完整安装、依赖、安全审查和验证证据见 `docs/NATURE_SKILLS_INSTALL_REPORT.zh-CN.md`。

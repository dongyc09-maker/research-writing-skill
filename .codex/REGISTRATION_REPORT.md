# Codex 注册验证报告

验证日期：2026-10-27。基线提交：6f79595。CLI：codex-cli 0.163.0。

## 结果与证据

19 个模块全部注册，未注册模块 0，发现验证失败模块 0。全部使用相对目录链接，保留原始 skills/、modules/、scripts/、templates/、plan-template/ 等资源。

实际调用 Codex app-server 的 initialize、skills/list，参数 cwds 为仓库根，forceReload=true。返回 scope=repo、enabled=true，errors=[]。默认状态目录只读导致初次探测启动失败；随后使用 work/codex-home 隔离状态目录成功，不使用模型或凭据。临时移走 .agents/skills 对照得到 0 个仓库技能，恢复后得到 19 个。探测进程初版退出等待超时已修正并复验。

网页会话的 executor 技能工具仍返回空清单，因此不能声称本网页会话已热加载；本报告证明当前 Codex CLI 的实际发现，合并后的网页新任务仍应核对技能清单。

| 模块 | 注册目标 | 实际发现 |
|---|---|---|
| brainstorming-research | `../../skills/brainstorming-research` | 已启用，repo |
| environment-setup | `../../skills/environment-setup` | 已启用，repo |
| evidence-driven-writing | `../../skills/evidence-driven-writing` | 已启用，repo |
| experiment-results-planning | `../../skills/experiment-results-planning` | 已启用，repo |
| figures-diagram | `../../skills/figures-diagram` | 已启用，repo |
| figures-python | `../../skills/figures-python` | 已启用，repo |
| latex-output | `../../skills/latex-output` | 已启用，repo |
| literature-review | `../../skills/literature-review` | 已启用，repo |
| paper-orchestration | `../../skills/paper-orchestration` | 已启用，repo |
| peer-review | `../../skills/peer-review` | 已启用，repo |
| prompts-collection | `../../skills/prompts-collection` | 已启用，repo |
| statistical-analysis | `../../skills/statistical-analysis` | 已启用，repo |
| using-research-writing | `../../skills/using-research-writing` | 已启用，repo |
| verification | `../../skills/verification` | 已启用，repo |
| writing-chapters | `../../skills/writing-chapters` | 已启用，repo |
| writing-core | `../../skills/writing-core` | 已启用，repo |
| writing-humanities | `../../skills/writing-humanities` | 已启用，repo |
| writing-law | `../../skills/writing-law` | 已启用，repo |
| writing-medical | `../../skills/writing-medical` | 已启用，repo |

根 SKILL.md 是旧平台兼容总索引，未作为第 20 个技能注册，避免重复入口；不是验证失败。入口使用 using-research-writing。

## 元数据、路径与完整性

全部模块有合法 YAML name、description；名称与目录一致且唯一。allowed-tools 为跨平台元数据，不作为 Codex 权限授予依据。

补充每个技能的真实路径解析规则，修复 writing-core 中硬编码仓库名的脚本路径。evidence-driven-writing 的 references/gpr-introduction-example.md 存在且从链接可访问；writing-chapters 的 brainstorming 模板、literature-review 的检索及 PDF 脚本均存在。plan/refs/figures/tables 等为论文运行时输出，不误判为缺失资源。

运行结果：check_codex_skills.py 通过全部 19 项元数据、链接、引用资源与发现结果检查，以及原 check_skill_integrity.ps1 的 45 项内容断言和必需文件检查；Python 脚本 AST 语法检查通过；Bash 脚本与 session-start 的 bash -n 通过。环境没有 pwsh，未直接执行 PS1；Python 检查等价移植其声明的完整性断言，不宣称运行过 PowerShell。research_quality_gate.ps1 是稿件检查，本任务无稿件，不适用。

## 依赖与重点技能

- literature-review：requests；可选 PDF 解析需 PyMuPDF；访问 Crossref、PubMed、Semantic Scholar、arXiv。检索得到元数据仍需核实原文与 DOI。
- evidence-driven-writing：依赖 literature-review 的来源池和 evidence map；附带本地示例，无额外安装。
- writing-chapters：依赖入口、brainstorming、writing-core、证据与章节提纲；中型或整篇写作由 paper-orchestration 编排。
- peer-review：以稿件、方法、统计和引用证据为输入，配合 verification；无需注册时安装依赖。
- figures-python：Python、matplotlib、seaborn、numpy、pandas，按统计需要补 scipy 等；必须保留 data manifest 与 mock 边界。Conda 不是技能发现前提。
- 其余模块为 Markdown 指导及仓库模板；LaTeX 输出按需使用外部编译器，环境技能仅在确有环境需求时使用。

## 安全审查与执行边界

静态审阅 scripts/、hooks/ 及技能中的命令。检索脚本向外部数据库发送查询，可将结果写入调用者指定路径；不在注册阶段运行。arXiv 仍使用 HTTP，存在传输完整性风险，使用前应改为 HTTPS 并检查响应。PDF 解析器处理不可信文件，需维护已修复版本的 PyMuPDF，并限制文件大小与资源。脚本输出路径可覆盖已有文件，调用前确认目标。

environment-setup 含 latest 安装器下载执行、conda init 和全局 pip 源修改。已加明确约束：固定版本、校验官方 SHA-256、按需安装，不原样自动执行。没有运行安装器、pip/conda 安装或全局配置修改。

init_plan 只按需创建计划与复制缺失模板；style_check 只读扫描；质量门脚本检查稿件并有 SelfTest 临时夹具逻辑。本次仅运行已审查的完整性与发现检查。hooks/session-start 会注入入口内容，但本次没有注册或执行 hook。原始资源均保留。

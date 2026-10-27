# 双科研技能库安装与验证报告

核查日期：2026-10-27（北京时间）。目标仓库：
`dongyc09-maker/research-writing-skill`。

本次提交在独立分支 `integrate/nature-skills-persistent` 整合 Nature Skills。
合并前 main 不包含这些新增文件；审核合并后，新云端任务检出最新 main 即可取得完整资源。
技能文件的持久化不等于所有 Python/R/MCP、数据库权限或付费服务都已配置。

## 1. 基线与上游核查

- 项目以 GitHub 最新 main `1613e5fc89fff5fedca38ba94688682cfbce2af1` 为基线。
  初始云端目录停留于 `6f79595`，缺少最近的 Codex 注册工作；已取得最新 main 后再整合。
- 基线已有 `.agents/skills/` 下 19 个相对目录链接、`.codex/INSTALL.md`、
  `.codex/REGISTRATION_REPORT.md` 和历史发现证据。
- 本次重新运行基线检查：19 个模块元数据、注册和资源检查通过；原完整性脚本的
  45 项内容断言通过；实际 `skills/list` 发现 19 个启用的 repo 技能，errors=[]。
  历史报告保留原样，本报告及下列新证据代表本次新增验证。
- 已核查 Nature Skills 的 README.md、README_EN.md、README 技能索引、SKILL.md
  元数据、所选 10 项的完整入口、manifest 与依赖。上游固定提交：
  `c1637a89c7097d486ba1c6e755e34d01cbb24998`。
- 上游索引为 23 个可触发技能，另有 `nature-shared` 支持包。
  不能把目录名一律当作实际调用名，例如 `nature-proposal-writer` 的
  frontmatter name 是 `researchwrite`，本次未安装该项。
- README 的 `npx skills` 方式省略 `--global` 可项目安装；
  `scripts/update-codex-skills.sh` 默认复制到 `~/.codex/skills/`，不是本次方案。
  Python/R/MCP 不随技能文件自动安装。未运行 npx、上游安装器或更新器。

## 2. 原有 19 个技能：全部保留

下表所有条目继续从 `.agents/skills/<名称>` 指向 `../../skills/<名称>`。
原 `skills/` 的内容和 19 个原注册链接相对于基线均无改动。

| 原有技能 | 主要用途 | 本次验证 |
|---|---|---|
| using-research-writing | 入口、规则和路由 | 静态通过；实际发现 |
| paper-orchestration | 任务包、阶段与能力使用审计 | 静态通过；实际发现 |
| brainstorming-research | 选题、类型和结构 | 静态通过；实际发现 |
| evidence-driven-writing | 文献驱动写作与 evidence map | 静态通过；实际发现 |
| writing-chapters | 章节写作 | 静态通过；实际发现 |
| experiment-results-planning | 实验、结果与 mock 边界 | 静态通过；实际发现 |
| writing-core | 通用写作原则 | 静态通过；实际发现 |
| writing-medical | 医学写作 | 静态通过；实际发现 |
| writing-law | 法学写作 | 静态通过；实际发现 |
| writing-humanities | 人文写作 | 静态通过；实际发现 |
| literature-review | 文献综述 | 静态通过；实际发现 |
| latex-output | LaTeX 输出 | 静态通过；实际发现 |
| figures-python | Python 图表 | 静态通过；实际发现 |
| figures-diagram | 流程图、架构图 | 静态通过；实际发现 |
| statistical-analysis | 统计分析 | 静态通过；实际发现 |
| peer-review | 自审 | 静态通过；实际发现 |
| prompts-collection | 润色、翻译等提示词 | 静态通过；实际发现 |
| verification | 完整性和稿件质量验证 | 静态通过；实际发现 |
| environment-setup | 按需运行环境配置 | 静态通过；实际发现 |

新增名称与上述技能没有冲突。功能相近的技能保持并存，没有改名或覆盖。
今后若出现名称冲突，先报告，保留两库原文件，选择显式前缀 wrapper 等方案后再实施。

## 3. 新增技能和实际路径

所有新增注册均为 Git 模式 `120000` 的相对链接：

```text
.agents/skills/<名称>
  -> ../../third_party/nature-skills/skills/<名称>

实际入口：third_party/nature-skills/skills/<名称>/SKILL.md
```

| 新增 frontmatter name | 用途 | 仓库内依赖/执行条件 |
|---|---|---|
| nature-academic-search | 多源检索、引文管理、DOI 与他引审计 | 自带 MCP server、scripts、manifest、static、references；不依赖 prose shared 层 |
| nature-ref-verifier | 参考文献字段级多源核验 | 本地规则与 references；数据库/Web/Zotero 按可用性启用 |
| nature-paper-xray | 推理、设计、公式和证据边界精读 | 按需读取 nature-shared 的 paper-type-taxonomy |
| nature-paper-card | 01–16 节精读卡 | manifest 的 terminology-ledger 依赖 nature-shared；PDF/source map 必须使用捆绑 preparer 和 auditor |
| nature-reader | 中英对照、图文与公式、来源锚点 | nature-shared 的 terminology-ledger；源格式 fragments；公式验证脚本 |
| nature-writing | 证据约束的章节、论证、初次投稿材料 | nature-shared 的文体、伦理、术语、期刊格式等；按轴选 fragments |
| nature-polishing | 保持事实与强度的润色、翻译和压缩 | nature-shared 的文体、伦理、术语、跨稿一致性；排版另走 layout 规则 |
| nature-figure | Python/R 科研图、示意图与渲染 QA | 本地 assets/templates/scripts；期刊和论证规则按需依赖 nature-shared |
| nature-reviewer | 模拟审稿、分级关切与事后一致性审计 | nature-shared 的 consistency-sweep；三份互盲报告需要独立上下文 |
| nature-shared | 共享规则、期刊、术语、一致性脚本 | 仅支持包，不独立接收用户科研任务 |

保留的是所选技能的全部 Git 跟踪文件，包括隐藏文件、测试、README、references、
static、manifest.yaml、scripts、assets、templates、agents、MCP server 和配置示例；
相邻的 nature-shared 完整保留。另保留上游根 LICENSE、双语 README、docs、scripts
供追溯。共 435 个文件，约 36.5 MB；无嵌套 .git、子模块或 LFS 下载前置条件。
上游根 README 中未复制的宣传图片不属于技能运行依赖。

锁文件 `third_party/nature-skills.lock.json` 逐项记录 blob SHA-1 和模式。
`check_nature_skills.py` 校验全部文件原始字节、文件模式、目录清单和 170 个入口/manifest
直接引用资源。SKILL.md 和 manifest 中的共享引用均可在真实目录下读取。
其余 Markdown 链接扫描仅发现 reader 文档中的 `assets/fig1.png`、
`assets/equations/E001.png` 等产出示例，不属于漏装的捆绑资源。

本次没有安装其余 14 个上游目录：nature-citation、nature-data、nature-downloader、
nature-experiment-log、nature-image2ppt、nature-literature-pipeline、nature-paper-to-patent、
nature-paper-trans、nature-paper2ppt、nature-paper2word、nature-proposal-writer（researchwrite）、
nature-response、nature-social-science、nature-statistics。
相关技能名在“Related skills”中的出现是推荐转交关系，不表示已安装；所选技能的
manifest 和本地必读资源没有依赖这些缺省目录。需要新增能力时再独立审查安装。

## 4. 调用方式和优先级

AGENTS.md 保留原约束并追加双库路由。Research Writing Assistant 负责总体流程、
SCI 综述证据组织、任务包、章节确认和质量门；Nature Skills 负责专项执行。
用户明确选择优先，系统/平台约束仍高于技能文件。

可直接请求：

```text
使用 nature-academic-search 检索这个主题，并用 nature-ref-verifier 核验最终参考文献。
使用 nature-paper-xray 讲透这篇论文的设计、公式和证据边界。
使用 nature-reader 生成中英对照 reader，再用 nature-paper-card 生成精读卡。
使用 Research Writing Assistant 组织 SCI 综述，结合 nature-writing 起草并保留 evidence map。
使用 nature-polishing 润色此段，保留数字、术语和论断强度。
使用 nature-reviewer 模拟审稿；如无法隔离上下文，请明确说明互盲限制。
使用 nature-figure，用 Python 绘图，保留数据清单并完成最终 PDF 的渲染 QA。
```

先从注册入口读取真实 SKILL.md；router 还要读取 manifest、always_load 和所选 fragment。
上游示例 `skills/nature-*/...` 在这里应解析为
`<本仓库>/third_party/nature-skills/skills/nature-*/...`，执行时使用绝对脚本路径。
不要从论文工作目录猜根目录，不要将产物写入 third_party。

## 5. 三层验证：结论和边界分别列出

| 层次 | 本次证据 | 能证明什么 | 尚不能证明什么 |
|---|---|---|---|
| 文件与资源可读取 | 原 19 项检查；新增 10 项元数据/链接；435 文件字节/模式；170 资源 | 全部所选技能和必读依赖已随仓库保存且可解析 | 没有证明任何数据库、模型或 API 可用 |
| 按指令执行 | 选中 citation-file-mgmt 分支并读取规则，实际离线转换捆绑完整记录；从注册真实路径运行 Paper Card preparer；reader 数学 QA 自测 | 引文转换、捆绑脚本、来源页码保护和本地 QA 能在项目内工作 | 没有完成真实论文 reader、整篇写作、付费绘图 API 或互盲审稿的端到端验收 |
| Codex 原生发现 | codex-cli 0.163.0 app-server initialize + skills/list，forceReload=true | 29 个 repo 技能 enabled=true，errors=[]；每个新增技能发现一次且路径正确 | 不代表当前网页会话已经热加载，也不能保证未来平台版本的行为 |

当前 CLI 实际名称形如 `research-writing-assistant:nature-reader`，frontmatter 仍为
`nature-reader`。检查脚本兼容该命名空间，并同时核对真实路径、repo scope 和 enabled，
没有靠改名技能文件解决平台显示差异。

本网页会话的 executor 技能清单返回空列表；因此当前任务只能报告按文件读取和 CLI
实际发现。合并后请在以本仓库为项目根的新网页版任务核对可用技能；如平台暂未加载，
AGENTS.md 提供显式文件读取后备路径，必须如实标明采用该路径。

离线执行结果：一条完整捆绑 MEDLINE 记录转换 RIS/BibTeX，作者顺序、条数及 DOI
保持一致；合成 source-map 的已知页码保留，无页码块没有被伪造为第 1 页；reader
数学验证内置正反例通过。另运行原上游 9 个 shared 一致性单测和 7 个 Paper Card
preparer 单测，全部通过。没有把合成夹具当成真实科研数据或精读成果。

静态审查：102 个上游 Python 文件 AST 解析通过；7 个 Bash 文件 `bash -n` 通过。
29 项 frontmatter 还由实际 YAML 解析器检查通过。自有修改通过 `git diff --check`；
上游副本原有 CRLF、行尾空白和文件末尾空行按原字节保留，未为格式检查改写第三方文件。
`.gitattributes` 对固定副本禁用文本换行转换，以便 Git 检出后继续核验原始哈希。
第三方 VIGIL 示例有 3 条 `\l` 非法转义 SyntaxWarning，尚不影响当前解析，不据此宣称
所有绘图示例兼容。环境无 PATH 中的 pwsh，执行 Python 兼容检查的原 45 项断言；
未声称直接运行过 PS1。当前无论文稿件，稿件 quality gate 不适用。

新增注册负对照：临时只移走 10 个 Nature 注册时，实际发现恰为原有 19 项；恢复链接。
全新检出复验结果与证据另见 `validation/nature-skills/fresh-checkout.json`。

证据：

- `validation/nature-skills/discovery.json`：实际发现结果（含原始命名空间/路径）。
- `validation/nature-skills/negative-control.json`：19 项负对照。
- `validation/nature-skills/offline-smoke.json`：离线执行范围及读取资源。
- `validation/nature-skills/fresh-checkout.json`：全新目录复验。

复现命令（从本仓库根运行，不安装依赖、不联网调用科研服务）：

```bash
python scripts/check_codex_skills.py
python scripts/check_nature_skills.py
python scripts/smoke_nature_skills.py
mkdir -p work/codex-home
CODEX_HOME="$PWD/work/codex-home" python scripts/probe_codex_discovery.py
python scripts/check_codex_skills.py --discovery-json work/discovery.json
python scripts/check_nature_skills.py --discovery-json work/discovery.json
```

实际发现需要目标环境已有 Codex CLI。隔离 CODEX_HOME 仅保存测试状态，不安装技能。
无须信任并启动项目 hooks；探测不提交模型任务、不需要 API Key。

## 6. 尚未配置的外部依赖

以下状态是本次环境快照，不承诺未来云端环境预装相同软件。

| 能力 | 按需依赖 | 本次配置与限制 |
|---|---|---|
| 纯文本阅读/写作/润色规则 | 模型和提供的科研材料 | 文件齐全；未进行真实稿件写作验收 |
| 学术检索 MCP | Python、mcp 1.x、requests、toml、lxml、pybliometrics、defusedxml；MCP 客户端注册 | 源码与 requirements 完整；未注册/启动 MCP、未安装包；系统 Python 缺 requests/toml/pybliometrics/defusedxml |
| PubMed / Crossref / arXiv | 数据库网络访问；PUBMED_EMAIL；可选 NCBI_API_KEY | 未配置个人邮箱和 key；未进行 live 检索；Crossref/arXiv 可按可用工具降级 |
| OpenAlex 无 MCP 检索 | 标准库脚本；可选 OPENALEX_API_KEY | 脚本保留；未调用 API，不保证匿名额度 |
| Scopus / ScienceDirect | pybliometrics、Elsevier 凭据及机构授权 | 均未配置；授权与限流另验，不能由技能安装推定 |
| Zotero / CNKI / Web of Science | Zotero API/MCP、用户库、机构浏览器登录或其他可用检索工具 | 未连接；缺失来源必须标记未核验 |
| PDF reader / Paper Card | PyMuPDF、必要的 OCR/版面提取、公式渲染工具 | 系统 Python 有 PyMuPDF 1.26.6；JSON preparer 已测试，未做真实全文验收 |
| Python 科研图 | numpy、matplotlib、seaborn、按任务需要的 pandas/scipy；PDF QA 用 PyMuPDF | 部分库已预装，未新增安装或绘制；完整导出/碰撞 QA 未端到端运行 |
| R 科研图 | R/Rscript、ggplot2/patchwork/ComplexHeatmap 等所选包 | 当前 Rscript 不可用，未安装；不得悄悄跨后端替代 |
| OpenRouter 示意图 | OPENROUTER_API_KEY、网络和相应计费权限 | 未配置、未调用；本次整合不授权发送稿件或图片到外部服务 |
| LaTeX / OCR | 具体引擎、字体、tesseract/Poppler 等 | 可执行文件部分存在；没有以其存在宣称排版流程通过 |
| 三份互盲审稿 | 相互隔离的审稿上下文和冻结报告流程 | 未运行审稿；同一上下文的三个角色不能称为互盲 |

上游 requirements 是兼容版本范围，未做完整运行依赖锁定或漏洞数据库审计。
已有 `/workspace/.research-env` 只是本任务环境，不写入仓库也不作为技能持久化前提；
其中 PyMuPDF 2.0 与上游 figure 的 `<2.0.0` 要求不同，未来实际运行需选择满足约束的
专用解释器。不要盲目复用环境包清单。技能发现本身只需文件和 Codex 支持。

## 7. 脚本、依赖与潜在风险

1. **安装和更新副作用**：academic-search/install.sh 面向 Claude，含 pip 安装、全局复制
   和配置写入；根更新器含 rsync --delete、目录切换/清理、可选 pull/prune，自动更新器
   会联网。本项目不运行、不挂 hook、不配置开机自动更新。第三方源码保留供审阅。
2. **对外发送内容**：搜索脚本会发送查询/标识符；OpenRouter 脚本会发送提示词、摘要、
   引用图片，并把请求载荷写入产物元数据。执行前按具体任务核对授权与数据范围，
   产物不进入本仓库。没有任何 API Key、账号令牌或私有 MCP 配置被添加。
3. **网络输入边界**：引文下载有固定主机检查，但重定向和数据源真实性仍需核查；
   图像响应 URL 的保护仅检查协议和字面本地主机/IP，不能当作完备 DNS/重定向 SSRF
   防护。自定义 API endpoint 也可能接收认证头，不能盲目采用不可信地址。
4. **文件写入**：转换、preparer、图像导出、JSON QA 报告可能覆盖指定目标；先检查输入
   和输出路径，在独立论文目录执行。PDF/图片是非可信输入，库版本和资源限制需维护。
   根 star-history 开发脚本还包含读取 gh token 的后备逻辑，本次仅静态审阅，不执行。
5. **许可**：根 LICENSE 为 Apache-2.0；figures4papers 的声明明确未发现上游许可，且
   旧声明文字仍提到 MIT。保留声明不等于获得修改、分发或发表授权；投稿优先原创模板，
   若复用这些外来素材，应另行核查并取得所需许可。这是本 PR 的明确残余风险。
6. **科研判断**：上游 Stable/Beta/Draft 是其自述状态，不是本项目验收结论。Crossref
   404 也不能单独证明 DOI 虚假，可能属于其他注册机构；多源核验必须记录来源和边界。
   AI 审稿不能代替编辑决定，文体经验不能当作官方期刊政策，期刊要求需按目标核实。
7. **平台和路径**：相对链接已在当前 Linux Codex CLI 验证；Windows/禁止符号链接的平台
   可能需要另做复制或 wrapper 兼容验证。不得把路径可读等同于网页自动发现。

维护时保留两库原约束；更新须同批审查依赖和共享包并重新跑上述验证，采用新分支/PR，
不自动跟随上游 main，也不直接修改本项目 main。

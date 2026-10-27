# find-skills 第 30 个技能入口安装报告

验证日期：2026-10-27（北京时间）。仓库：`dongyc09-maker/research-writing-skill`。

## 安装结果与保留范围

在独立分支 `integrate/find-skills` 中运行用户指定的项目级命令：

```bash
npx skills add vercel-labs/skills --skill find-skills -a codex --copy -y
```

安装成功，返回码 0；仅选择并复制 `find-skills`，生成 `skills-lock.json`。
新增入口为 `.agents/skills/find-skills/SKILL.md`，不是用户主目录的全局安装。
首次普通沙箱尝试无法连接网络代理；获准联网重试后安装成功，未采用手工降级。
npm 缓存和 Codex 探测状态放在 Git 忽略的 `work/`。

安装前确认 19 个 Research Writing Assistant 与 10 个 Nature 入口均存在，
逐个读取 SKILL.md 并记录相对链接及 SHA-256；安装后逐项相等，共 30 项。
原 29 项没有删除、覆盖或重装，原 `skills/` 与 Nature vendor 内容未改动。
`AGENTS.md` 仅追加技能发现说明，保留原双科研技能库流程及优先级。
校验器保留原 45 项内容断言，并加入新增副本、来源、字节及发现检查。

## 官方来源、元数据与安全审查

- 官方目录：<https://github.com/vercel-labs/skills/tree/main/skills/find-skills>
- 审查的固定提交：`533c7df02f9b4d913fb8eba553aa99d86103d1d4`。
- [固定版本 SKILL.md](https://github.com/vercel-labs/skills/blob/533c7df02f9b4d913fb8eba553aa99d86103d1d4/skills/find-skills/SKILL.md)
  与安装副本逐字节一致，Git blob 为 `a41bdd074bb587afd861332cf2f473f3154de4d7`。
- SKILL.md SHA-256：`c00eeea0e13e74fe4a9d84ba0a8542205a1b736d65f13134fe1a6647eb14976f`。
- YAML 仅含 `name: find-skills` 和 `description`；描述为发现、安装可扩展的 agent skills。
  不含 `allowed-tools`、账户或 API Key 配置，也没有捆绑脚本或执行型依赖。
- 功能流程：理解需求 → 查 skills.sh 榜单 → CLI 搜索 → 核查安装量、来源及星数 →
  推荐候选 → 用户同意后安装。它查找的是 agent 技能，不直接检索 SCI 文献。
- 原文包含 `npx skills update` 和 `-g -y` 全局安装示例。
  本仓库说明明确要求先获用户确认，不自动安装搜索结果、不全局安装、不批量更新原技能。
  原文未修改；技能文本不能授予平台之外的权限。
- 未发现要求泄露凭据、隐蔽执行或绕过审查的内容。此结论仅覆盖审查的 Markdown；
  npm CLI、外部索引和将来安装的候选仍是独立的信任边界，热度不等于安全或科研有效性。
- 上游 MIT 许可原文保存在 `third_party/find-skills.LICENSE`，固定来源与哈希在
  `third_party/find-skills.lock.json`。CLI 的 `skills-lock.json` 仅记录新增项，
  原两库继续使用原注册和 Nature 锁文件；不要把 CLI 锁文件误当成全部 30 项清单。

## 依赖与网络条件

本次 Node.js `v24.19.0`、npx `11.9.0`、CLI `skills@1.7.4`。
已读取实际 npm 包的 `engines`：Node.js `>=22.20.0`。
读取 Markdown 本身无需 Node.js；远程搜索需 Node.js、npx 及 npm / skills.sh 网络。
缺少安装器时仍可将经核验的官方 SKILL.md 保存到仓库同一路径，保留许可及来源，
通过分支和 PR 持久化；不应因此断言技能不可安装。

当前云环境使用 HTTP(S) 代理。npm 与 Git 能使用既有代理，但 Node 的 `fetch`
默认没有使用环境代理。最初五个查询均显示 `No skills found`，退出码仍为 0。
检查 CLI 的 `searchSkillsAPI` 实现发现：异常或非成功 HTTP 响应都被转换为空数组。
因此这些初次输出不能证明没有候选，也不能证明远程查询成功。

在同一环境启用 Node 24 官方环境代理支持后，以下命令均返回真实候选、安装量及链接：

```bash
NODE_USE_ENV_PROXY=1 npx skills find "citation verification"
NODE_USE_ENV_PROXY=1 npx skills find zotero
NODE_USE_ENV_PROXY=1 npx skills find "scientific data analysis"
```

此变量只让请求使用继承的代理，没有改写网络策略或关闭 TLS 校验。
其他机器应按其 Node 版本及网络要求配置；Node >=22.20.0 是本次 CLI 要求，
并不代表每个满足该版本范围的构建都支持同样的环境代理开关。

## 科研搜索实测与推荐边界

先读取 skills.sh 榜单，再执行上述三类查询，返回码均为 0，且有非空远端结果。
以下为 2026-10-27 的动态索引快照，安装量日后可能变化。

| 查询 | 相关命中 | 索引安装量 | 审查状态 |
|---|---|---:|---|
| citation verification | galaxy-dawn/claude-scholar@citation-verification | 1.5K | 仅搜索命中，未审查其源码，不作为已批准安装建议 |
| zotero | k-dense-ai/scientific-agent-skills@pyzotero | 2K | 仅搜索命中，未验证账户、脚本或 Zotero 服务 |
| scientific data analysis | k-dense-ai/scientific-agent-skills@exploratory-data-analysis | 2.2K | 已阅读上游 SKILL.md，可优先评估，未安装、未执行其分析脚本 |

可优先评估 [K-Dense 的 exploratory-data-analysis](https://skills.sh/k-dense-ai/scientific-agent-skills/exploratory-data-analysis)：
其上游 SKILL.md 定义有界本地数据检查、缺失值/泄漏审计及分析报告，并要求保持原始数据。
已核查 [源仓库](https://github.com/K-Dense-AI/scientific-agent-skills) 和技能原文；
GitHub 页面约 54.8K 星，skills.sh 页面缓存约 54.6K 星，二者为不同更新时间的近似值。
来源为 K-Dense 第三方库，不是 Vercel 官方技能。核心脚本要求 Python 3.11+，
完整可选依赖快照要求 Python 3.12+、uv 和相关库。
本次只做需求匹配与文本审查，尚未审计脚本或验证其科研输出。

供以后确认后使用的项目级命令（本次未执行）：

```bash
npx skills add k-dense-ai/scientific-agent-skills --skill exploratory-data-analysis -a codex --copy -y
```

不建议仅凭热度安装同名 `statistical-analysis`：本仓库已存在该名称，需先解决冲突。
现有 `nature-ref-verifier`、`nature-academic-search`、`statistical-analysis` 仍按原科研路由使用。
本次没有安装任何搜索到的第三方候选。

## 三种验证结果

| 验证层次 | 结果 | 证据与范围 |
|---|---|---|
| SKILL.md 文件可读取 | 通过 | 读取副本、核对 name/description、固定提交及 blob；原 29 项链接和内容哈希不变 |
| 搜索命令可运行且查询远端 | 通过，有网络条件 | 初次代理未启用时输出误导性空结果；启用 `NODE_USE_ENV_PROXY=1` 后三类查询均返回候选；不等于实际执行候选功能 |
| Codex CLI 原生发现 | 通过 | codex-cli 0.163.0 的 app-server `skills/list`，`forceReload=true`；30 项均 repo/enabled，errors 为空 |
| 当前网页会话热加载 / 未来新会话 | 未验证 | 独立 CLI 发现不能代替网页会话的技能目录；合并后新任务需检出最新 main 再验证 |

CLI 实际返回的新技能名称为 `research-writing-assistant:find-skills`，
路径为仓库 `.agents/skills/find-skills/SKILL.md`。前缀由当前 Codex 构建添加，
官方 frontmatter 名称仍为 `find-skills`。

可重放的检查命令：

```bash
mkdir -p work/codex-home
CODEX_HOME="$PWD/work/codex-home" python scripts/probe_codex_discovery.py
python scripts/check_codex_skills.py --discovery-json work/discovery.json
python scripts/check_nature_skills.py --discovery-json work/discovery.json
```

两个检查均通过。Nature 原有 435 个文件字节/权限及 170 个引用资源检查保持通过。
证据见 `docs/validation/find-skills/`；discovery.json 只保留原响应中的 repo 项，
移除与本任务无关的 system 项，其他字段保留。临时状态、缓存和凭据不提交。

## 今后的调用方法

在包含本分支或合并后 main 的检出中，可以说：

> 用 find-skills 查找 SCI 论文的文献管理、引用核验或科研数据分析技能，只推荐，不安装。

若当前平台没有热加载，明确读取 `.agents/skills/find-skills/SKILL.md` 后按指引搜索，
报告“按指令读取执行”；只有实际的原生发现证据才可报告原生发现。
普通论文写作继续先走 `using-research-writing` 和原双库路由。
以后升级通过独立 PR 复核上游、许可、CLI 要求和搜索行为，不自动批量更新。

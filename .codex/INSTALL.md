# Codex 云端项目：仓库级持久化注册

本仓库已将 19 个模块逐个注册到 `.agents/skills/<name>`，每个均为指向
`../../skills/<name>` 的相对目录符号链接。链接与目标一起纳入 Git；云端任务
检出包含本修改的分支即可发现，无须安装 Python 包、运行 hook 或修改主目录。
不要将整个 `skills/` 目录当成一个技能链接，也不要只凭 `ls` 声称发现成功。

## 合并后使用

在 Codex 网页版选择此仓库及包含注册提交的 main 分支，创建新任务，工作目录
设在仓库内。已打开的会话可能保留旧技能快照，需新建任务。

可直接输入：

- `请使用 $using-research-writing 规划我的科研写作任务。`
- `请使用 $literature-review 整理我提供的文献，先建立证据映射。`
- `请使用 $evidence-driven-writing 根据证据映射起草引言。`
- `请使用 $writing-chapters 撰写已确认提纲中的下一章。`
- `请使用 $peer-review 检查我的稿件。`
- `请使用 $figures-python 根据真实 CSV 数据绘图。`

若界面展示带命名空间的技能名称，请使用实际清单中的全名。本次 CLI 返回
`research-writing-assistant:<name>`；例如 `$research-writing-assistant:literature-review`。
路径和资源规则见各 SKILL.md。用户论文输出路径应明确指定。

## 检查

```bash
python scripts/check_codex_skills.py
```

这只检查元数据、链接和资源及原 PS1 的完整性断言，不能证明运行时发现。
若当前环境有 Codex CLI，可在仓库根目录运行以下只读发现探测（不会启动模型）：

```bash
mkdir -p work
python scripts/probe_codex_discovery.py
python scripts/check_codex_skills.py --discovery-json work/discovery.json
```

探测调用 `initialize`、`skills/list`（仓库 cwd，`forceReload: true`）。默认 Codex
状态目录不可写时，可为该命令指定独立可写状态目录，不复制凭据：

```bash
mkdir -p work/codex-home
CODEX_HOME="$PWD/work/codex-home" python scripts/probe_codex_discovery.py
```

该结果验证安装的 CLI 发现机制；隔离状态目录不代表当前网页会话已刷新。
本次实际结果、依赖与安全审查见 [注册报告](REGISTRATION_REPORT.md)。

## 依赖

发现技能只需要检出仓库并保留 Git 符号链接。Python 3 用于跨平台检查；
PowerShell 可选，用于原 `scripts/check_skill_integrity.ps1` 和稿件质量门。
按任务需要才安装 `requests`（文献检索）、PyMuPDF（PDF）、
matplotlib/seaborn/numpy/pandas（绘图）、scipy/statsmodels 等（统计），
LaTeX 工具链用于编译。无需为了注册安装 Conda。

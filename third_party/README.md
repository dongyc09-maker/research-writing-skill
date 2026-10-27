# Nature Skills 固定版本副本

来源：<https://github.com/Yuan1z0825/nature-skills>，提交
`c1637a89c7097d486ba1c6e755e34d01cbb24998`（2026-10-27 核查）。

`nature-skills/` 是所选 10 个技能的完整、未经修改的文件副本，不是 Git 子模块。
同时保留上游 LICENSE、中英文 README、docs 和根 scripts 供追溯；根安装/更新脚本
不属于本项目启动流程。没有 `.git`、运行环境、账号配置或自动更新 hook。

`.agents/skills/nature-*` 通过相对目录链接注册，技能内部相邻的 `nature-shared`
依赖保持上游布局。`nature-skills.lock.json` 记录固定提交、范围、435 个文件的
Git blob SHA-1 和文件模式；`python scripts/check_nature_skills.py` 离线校验。
锁文件用于复现和发现本地漂移，并不替代来源审查或包供应链审计。

根 LICENSE 为 Apache-2.0。嵌套的 `figures4papers/THIRD_PARTY_NOTICES.md`
明确其素材没有已知明确许可证，且旧文字仍提及 MIT；应按该文件的限制单独处理，
不能用本项目或 Nature Skills 根许可推定获得素材授权。

升级时在新分支核查上游 README、每个 SKILL.md、manifest、共享依赖、脚本和许可；
重新保存完整所选目录并更新锁文件，复验原库、新库、离线冒烟和实际发现，再走 PR。
不要直接在此副本运行上游自动更新器，不要把本项目仓库当作上游 clone 执行 `--pull`。

本项目使用方式和外部依赖见 [中文安装报告](../docs/NATURE_SKILLS_INSTALL_REPORT.zh-CN.md)。

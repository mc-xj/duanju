# 项目操作约定

默认在 `main` 分支读取与操作，除非用户另行指定。不要自动合并其他分支。

用户已授权：今后在本项目完成文件新增、修改、重命名或删除并检查后，自动提交并推送到 GitHub 仓库 `mc-xj/duanju` 的当前工作分支（默认 `main`），无需再次询问。纯读取操作不创建提交；用户当次明确要求不提交或不推送时，以当次要求为准。推送遇到远端分歧时，不强制推送或覆盖他人提交。

## 项目技能

技能安装在 `.agents/skills/`。用户点名时读取对应SKILL.md，并按照用户当前请求使用；安装不等于自动启用持续模式。

- `$caveman`：`.agents/skills/caveman/SKILL.md`，精简回答，停止用 `stop caveman`。只安装核心技能，不包含ultracave/megacave。
- `$markitdown`：`.agents/skills/markitdown/SKILL.md`，提取本地文档为Markdown。
- `$ppt-master`：`.agents/skills/ppt-master/SKILL.md`，制作与编辑PPT，包内包含脚本、参考和模板。
- `$harness-anything`：`.agents/skills/harness-anything/SKILL.md`，跨平台办公CLI与LibreOffice转换，Linux限制见入口。

技能依赖使用项目的 `.venv-tools`。如果不存在且任务需要执行工具，先运行 `bash scripts/setup_skills.sh`，再运行 `./.venv-tools/bin/python scripts/check_skills.py`。不要将虚拟环境提交Git。

优先使用对应入口中的命令。不要运行PPT Master的update_repo.py更新本项目仓库；其上游更新器假定独立checkout。更新技能时单独审核上游，并更新源码版本与依赖锁。

完整技能和源码已随仓库存储，环境重建无需重新下载技能仓库。可在云环境安装脚本中设置 `bash /workspace/duanju/scripts/setup_skills.sh` 恢复依赖。保留现有环境脚本时追加此命令，不替换未知配置。

Behavioral guidelines to reduce common LLM coding mistakes. Merge with project-specific instructions as needed.

**Tradeoff:** These guidelines bias toward caution over speed. For trivial tasks, use judgment.

## 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

## 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

## 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

## 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

---

**These guidelines are working if:** fewer unnecessary changes in diffs, fewer rewrites due to overcomplication, and clarifying questions come before implementation rather than after mistakes.

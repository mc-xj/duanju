# 项目操作约定

默认在 `main` 分支读取与操作，除非用户另行指定。不要自动合并其他分支。

## 项目技能

技能安装在 `.agents/skills/`。用户点名时读取对应SKILL.md，并按照用户当前请求使用；安装不等于自动启用持续模式。

- `$caveman`：`.agents/skills/caveman/SKILL.md`，精简回答，停止用 `stop caveman`。只安装核心技能，不包含ultracave/megacave。
- `$markitdown`：`.agents/skills/markitdown/SKILL.md`，提取本地文档为Markdown。
- `$ppt-master`：`.agents/skills/ppt-master/SKILL.md`，制作与编辑PPT，包内包含脚本、参考和模板。
- `$harness-anything`：`.agents/skills/harness-anything/SKILL.md`，跨平台办公CLI与LibreOffice转换，Linux限制见入口。

技能依赖使用项目的 `.venv-tools`。如果不存在且任务需要执行工具，先运行 `bash scripts/setup_skills.sh`，再运行 `./.venv-tools/bin/python scripts/check_skills.py`。不要将虚拟环境提交Git。

优先使用对应入口中的命令。不要运行PPT Master的update_repo.py更新本项目仓库；其上游更新器假定独立checkout。更新技能时单独审核上游，并更新源码版本与依赖锁。

完整技能和源码已随仓库存储，环境重建无需重新下载技能仓库。可在云环境安装脚本中设置 `bash /workspace/duanju/scripts/setup_skills.sh` 恢复依赖。保留现有环境脚本时追加此命令，不替换未知配置。

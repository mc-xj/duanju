# 项目技能安装与调用

技能文件位于 `.agents/skills/`；底层Python工具使用 `.venv-tools/`。技能源码、入口、许可证、版本信息和依赖锁随Git保存；虚拟环境及缓存不提交。

## 调用方法

| 名称 | 聊天调用示例 | 安装位置 |
| --- | --- | --- |
| Caveman | `$caveman` 或“使用caveman精简回答” | `.agents/skills/caveman/` |
| MarkItDown | `$markitdown 读取这份分镜Word` | `.agents/skills/markitdown/` |
| PPT Master | `$ppt-master 根据主分支内容制作答辩PPT` | `.agents/skills/ppt-master/` |
| Harness Anything | `$harness-anything 把这份DOCX转换成PDF` | `.agents/skills/harness-anything/` |

当前聊天不一定刷新技能菜单；可直接点名技能让助手读取本地SKILL.md，或重新打开此项目会话后查看技能列表。此安装不修改全局助手配置，不自动激活Caveman持续模式。Caveman停止指令为 `stop caveman`。

PPT Master为完整6.9.0技能包；Caveman仅包含核心技能，不包含ultracave或megacave。MarkItDown和Harness的项目入口为本地适配，不冒充上游发布的SKILL.md。

## 恢复环境

项目根目录执行：

```bash
bash scripts/setup_skills.sh
.venv-tools/bin/python scripts/check_skills.py
```

云环境设置中的安装脚本可追加：

```bash
bash /workspace/duanju/scripts/setup_skills.sh
```

现有云环境配置没有被本次安装覆盖或发布。AGENTS.md会提醒助手在工具缺失时执行恢复脚本。恢复依赖需要访问Python包源；LibreOffice转换还要求环境PATH中存在soffice或libreoffice。当前环境已提供soffice。

## 实际命令

```bash
# 读取文档为Markdown
.venv-tools/bin/markitdown '02_逐场独立分镜/第01段_雨夜翻页_超详细分镜.docx' -o /tmp/分镜.md

# PPT Master入口完整性检查
.venv-tools/bin/python .agents/skills/ppt-master/scripts/attribution_guard.py

# 查看Harness命令
.venv-tools/bin/cli-anything-office --help

# 使用Harness的LibreOffice后端转换已有文件，拒绝覆盖已有输出
.venv-tools/bin/python scripts/harness_convert.py /path/source.docx /path/result.pdf
```

## 审核范围与权限

审核了各工具的入口指令、包配置、安装方式及本次使用路径。PPT Master完整技能包保留其归属文件、校验器和模板，未绕过上游校验。审核不是整个第三方项目及所有依赖的完整安全审计。

- Caveman为静态文字指令；未运行完整安装器、未安装遥测CLI或用户级钩子。
- MarkItDown以当前进程权限读写文件，支持网络输入；本项目测试只用本地文件，第三方插件和云客户端未启用。
- ONNX Runtime导入时提示无法持久化遥测设备ID；测试随后调用disable_telemetry_events。没有进行网络抓包，不能宣称所有依赖绝无遥测。
- PPT Master部分可选功能依赖联网API，如图像或语音生成；安装相关依赖不代表已经配置服务。没有写入API密钥，没有启动本地Web服务。
- PPT Master依赖包括PyMuPDF等，其许可证独立于技能本身MIT许可。安装依赖到本地虚拟环境，不将依赖二进制打包进Git。
- Harness原主版依赖Windows COM；这里使用同作者跨平台版本。经代码检查，跨平台版的`export render`仍依赖COM，Linux不可作为完整WPS替代。本地入口明确避开该路径，复用其现有LibreOffice转换函数。HTML转DOCX自动过滤器在本机不适用；HTML转PDF测试通过，其他组合以实际过滤器支持为准。
- Harness不安装Adobe或Zotero桌面集成、不关闭应用、不改动现有文档；本地转换目标存在时拒绝覆盖。

具体上游版本与技能入口哈希见 `skill-sources.json`。不要运行技能包的update_repo.py更新本项目；如需升级，应单独审核和替换技能快照。

## 测试结果

`check_skills.py`为可重复执行的本地冒烟测试，所有临时文件位于独立临时目录，不更改剧本或分镜。

| 测试 | 结果 |
| --- | --- |
| 四个技能name/description入口 | 通过 |
| Caveman核心指令与上游一致，无钩子安装 | 通过；静态检查，未测量token收益 |
| pip check | 通过，无依赖冲突 |
| PPT Master归属完整性检查 | 通过 |
| PPT Master原生SVG文字转可编辑PPTX，读取PPTX验证中文 | 通过 |
| MarkItDown转换第一段中文分镜Word，验证标题和镜号 | 通过，提取6693字符 |
| Harness CLI创建并修改JSON文档项目 | 通过 |
| Harness LibreOffice后端HTML转PDF，读取PDF验证中文 | 通过 |
| Harness已有输出文件防覆盖 | 通过 |

上游云API、完整PPT策划流程、Windows COM及宿主技能菜单自动发现没有在此次测试中验证。

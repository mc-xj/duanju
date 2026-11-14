---
name: harness-anything
description: 使用Harness Anything跨平台办公工具编辑JSON文档项目，或通过LibreOffice转换本地Office文件。适用于文档、表格及演示文件自动化请求。
---

# Harness Anything 项目入口

这是本项目编写的适配入口。原项目为yb2460/harness-anything；本Linux环境安装同作者的harness-anything-mac跨平台版本。上游原技能保存在references/upstream-office-skill.md，仅作参考；其中的Windows命令不能直接用于Linux。

从本技能位置定位项目根目录（向上三级）。若 `.venv-tools/bin/cli-anything-office` 缺失，执行 `bash scripts/setup_skills.sh`。

## 查看与编辑JSON项目

```bash
.venv-tools/bin/cli-anything-office --help
.venv-tools/bin/cli-anything-office document new --type writer --name '文档' -o /tmp/document.json
.venv-tools/bin/cli-anything-office --project /tmp/document.json writer add-paragraph --text '正文'
```

命令的选项以 `--help` 为准。对现有项目先备份，未经授权不覆盖文件。

## Linux下转换已有文件

```bash
.venv-tools/bin/python scripts/harness_convert.py '/path/input.docx' '/path/output.pdf'
```

此适配脚本直接调用上游office_backend.convert_to，要求PATH中有soffice或libreoffice，目标文件已存在时拒绝覆盖。支持范围取决于本机LibreOffice过滤器。

## 边界

- 跨平台仓库的 `export render` 仍走Windows COM；Linux下不要调用它导出JSON项目，也不要声称全套WPS命令已兼容。
- 无Office文件时，可用JSON命令整理内容；需要生成正式Word/PPT时使用本机文档/演示工具或PPT Master，不把JSON冒充Office文件。
- 不执行原Windows技能中的taskkill，不关闭用户应用，不直接写Zotero数据库，不安装Photoshop/Illustrator COM组件。
- 默认仅本地读写和本地LibreOffice子进程，不上传文件。

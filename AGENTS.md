# Repository Guidelines

## 项目结构与模块
- `GrandConcourse.py`：入口脚本；运行前设置目标 ID（如 `question_id`、`article_id`）和 `warehouse` 输出路径。
- `zhihu/`：按领域分模块（`question`、`article`、`topic`、`collection`、`user`），负责调用 API、解析并生成 Markdown。
- `util/`：公用工具（`net` 处理 HTTP 与 API 组装，`const` 存放请求头与常量，`parse` 将 HTML 转 Markdown，`timer` 控制节奏，`document` 生成 Markdown 文件）。
- `API 返回样例/`：API 返回示例，便于对照字段格式；`design/爬虫.xmind` 描绘流程，改动抓取行为时同步更新。

## 构建、测试与开发命令
- 建议 Python 3.11（见 `.python-version`），使用虚拟环境：`python -m venv .venv && source .venv/bin/activate`（Windows 用 `Scripts\\activate`）。
- 安装运行依赖：`pip install requests beautifulsoup4 lxml`。
- 运行爬虫：填好 ID 后执行 `python GrandConcourse.py`，Markdown 输出到 `warehouse`。
- 若新增解析入口，可运行 `python -m util.parse.simple` 等自测；或在 `util/parse/guidance` 下放置小脚本做烟囱测试。

## 代码风格与命名
- 遵循 PEP 8，4 空格缩进；函数尽量单一职责。
- 网络请求集中于 `util/net`，解析集中于 `util/parse`，Markdown 组装在 `util/document`，业务编排在 `zhihu/*`。
- 文件/模块使用小写加下划线；生成的 Markdown 文件名模板见 `document.py`，确保字符可在各平台安全保存。

## 测试指引
- 目前无完整自动化套件；为新增解析器或 API 组装函数补充轻量 `unittest`。
- 优先使用 `API 返回样例/` 的离线数据构造用例，避免频繁请求知乎。
- 新增爬虫路径时提供可离线运行的最小命令，并记录在 PR 描述或对应脚本注释中。

## 提交与 PR 规范
- 提交信息使用简洁祈使句（如 `feat: add topic crawler`、`fix: handle empty content`），单次提交聚焦单个变更。
- PR 需说明目标知乎实体（问题/用户/收藏夹 ID）、新增请求头或限速策略、产出 Markdown 的示例路径。
- 给出复现步骤和执行命令；调整格式时可附上生成的 Markdown 片段。
- 禁止提交敏感信息（Cookie、Token 等）；`util/const` 中的头信息保持通用模板。

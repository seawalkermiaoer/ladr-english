# 项目概览

本仓库包含两个子项目：

- `gen-audio`：离线将英文/中英文文章合成为音频，并生成时间轴标记与 Markdown 播放清单
- `obsidian-word-gpt`：配合 Obsidian 插件的单词记忆工具；本次新增一个 `FastAPI` 后端（位于 `obsidian-word-gpt/backend`）用于本地词库与复习记录管理

# 目录结构

```
gen-audio/
  main.py                  # 音频生成与合并流程
  res/                     # 生成的音频与时间轴输出（运行后产生）
  tmp/                     # 中间文件（运行时生成）

obsidian-word-gpt/
  src/                     # Obsidian 插件前端源码（TS/Svelte）
  backend/                 # FastAPI 后端（本地 SQLite 词库与复习接口）
```

# 快速开始

## 1. gen-audio（文章离线合成音频）

输入文件为 JSON 数组，每项包含英文与中文：

```
[
  {"english": "Hello", "chinese": "你好"},
  {"english": "World", "chinese": "世界"}
]
```

运行：

```
python gen-audio/main.py input.json          # 使用指定输入
python gen-audio/main.py --input data.json   # 使用 --input 方式
python gen-audio/main.py data.txt --base x1  # 指定输出基础名
```

输出文件位于 `gen-audio/res/`：

- `*.wav` 与 `*.mp3`：合并后的音频
- `*.step2.json`：每句的开始/结束时间戳
- `*.md`：Markdown 播放清单（带可视化时间范围）

依赖：需本机安装 `ffmpeg` 与可用的 TTS 服务（代码默认指向本地兼容接口）。

## 2. obsidian-word-gpt 后端（FastAPI）

后端位于 `obsidian-word-gpt/backend`，提供本地词库管理与复习记录接口，默认使用 SQLite。

安装依赖并启动：

```
cd obsidian-word-gpt/backend
python -m venv .venv && .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

开放的主要接口示例：

- `GET /health`：健康检查
- `POST /api/words`：新增单词
- `GET /api/words`：分页/搜索单词列表
- `GET /api/words/{id}`：获取单词详情
- `PUT /api/words/{id}`：更新单词
- `DELETE /api/words/{id}`：删除单词
- `POST /api/words/{id}/review`：记录一次复习（支持简易间隔算法字段）
- `GET /api/stats`：词库统计信息

跨域：为便于 Obsidian 插件本地开发，后端默认允许本机来源跨域访问。

# 测试与规范

- 代码风格：遵循 Google 代码规范，类型标注与文档字符串完整
- Python 单元测试：后端使用 `pytest`，覆盖率目标 ≥ 80%

运行测试：

```
cd obsidian-word-gpt/backend
pytest --maxfail=1 --disable-warnings -q
```

# 许可

本仓库使用与上游一致的 `LICENSE` 文件。

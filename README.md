# Seedance Video Generation Skill

基于 [Volcengine Seedance API](https://www.volcengine.com/docs/ark/seedance-video) 的 Claude Code skill，提供文生视频（Text-to-Video）和图生视频（Image-to-Video）功能。

## 功能特性

- ✅ **文生视频**（T2V）- 从文本描述生成视频
- ✅ **图生视频**（I2V）- 从图像生成视频动画
- ✅ **首尾帧模式** - 使用首尾图像生成过渡动画
- ✅ **参考图像模式** - 使用多张参考图像控制输出
- ✅ **草稿模式**（Seedance 1.5 Pro）- 快速预览后再生成高质量视频
- ✅ **音频生成**（Seedance 1.5 Pro）- 从文本自动生成同步音频
- ✅ **任务管理** - 查询、列表、取消任务
- ✅ **轮询监控** - 自动等待任务完成并下载视频

## 安装

### 1. 克隆仓库

```bash
git clone https://github.com/zBlackIf/seedance-video-generation-skill.git
cd seedance-video-generation-skill
```

### 2. 安装依赖

```bash
pip install -r scripts/requirements.txt
```

### 3. 设置 API Key

在 [Volcengine 控制台](https://console.volcengine.com/ark) 获取 API Key，然后设置环境变量：

```bash
export ARK_API_KEY="your-api-key-here"
```

或在当前目录创建 `.env` 文件：

```
ARK_API_KEY=your-api-key-here
```

## 快速开始

### 文生视频

```bash
# 基本文生视频
python scripts/create_task.py --prompt "一只可爱的小猫在阳光下打哈欠"

# 自动下载到本地（默认 output/ 文件夹）
python scripts/create_task.py --prompt "一只可爱的小猫在阳光下打哈欠" --auto-download

# 指定下载目录
python scripts/create_task.py --prompt "一只可爱的小猫在阳光下打哈欠" --auto-download --output-dir ./videos
```

### 图生视频

```bash
# 单帧图生视频
python scripts/create_task.py \
  --prompt "镜头缓慢拉远展示全景" \
  --image /path/to/image.jpg

# 首尾帧模式
python scripts/create_task.py \
 1 --prompt "平滑过渡" \
  --image first.jpg \
  --last-frame last.jpg
```

### 查询任务状态

```bash
# 查询状态
python scripts/query_task.py <task_id>

# 轮询等待完成
python scripts/query_task.py --watch <task_id>

# 完成后自动下载
python scripts/query_task.py --watch <task_id> --download output.mp4
```

## 使用示例

### 自定义参数

```bash
python scripts/create_task.py \
  --prompt "海边日落，电影感" \
  --resolution 1080p \
  --ratio 21:9 \
  --duration 8 \
  --watermark false
```

### 带音频生成（Seedance 1.5 Pro）

```bash
python scripts/create_task.py \
  --prompt "厨师在餐厅烹饪，说：'菜好了！'" \
  --model doubao-seedance-1-5-pro-251215 \
  --generate-audio true
```

### 草稿模式（Seedance 1.5 Pro）

```bash
# 步骤 1: 生成快速预览
python scripts/create_task.py \
  --prompt "doubao-seedance-1-5-pro-251215 \
  --draft true

# 步骤 2: 基于草稿生成最终视频
python scripts/create_task.py \
  --model doubao-seedance-1-5-pro-251215 \
  --draft-task-id <draft_task_id>
```

### 参考图像模式（仅 Lite 模型）

```bash
python scripts/create_task.py \
  --model doubao-seedance-1-0-lite-i2v \
  --prompt "[图1]一个人戴着[图2]红色帽子" \
  --reference-images ref1.jpg,ref2.jpg
```

## 可用模型

| 模型 ID | 类型 | 分辨率 | 特性 |
|---------|------|--------|------|
| doubao-seedance-1-5-pro-251215 | Pro (最新) | 最高 1080p | T2V + I2V + 音频 + 草稿 |
| doubao-seedance-1-0-pro-t2v | Pro | 最高 1080p | T2V |
| doubao-seedance-1-0-pro-i2v | Pro | 最高 1080p | I2V + 首尾帧 |
| doubao-seedance-1-0-pro-fast-t2v | Fast | 最高 1080p | T2V（快速） |
| doubao-seedance-1-0-lite-t2v | Lite | 最高 720p | T2V |
| doubao-seedance-1-0-lite-i2v | Lite | 最高 720p | I2V + 首尾帧 + 参考图 |

更多模型详情请参考 [references/models.md](references/models.md)。

## CLI 工具

### create_task.py

创建视频生成任务。

```bash
python scripts/create_task.py --help
```

主要参数：
- `--prompt` - 文本提示词
- `--image` - 首帧图像路径
- `--last-frame` - 尾帧图像路径
- `--reference-images` - 参考图像（逗号分隔）
- `--model` - 模型 ID
- `--resolution` - 480p/720p/1080p
- `--ratio` - 16:9/4:3/1:1/3:4/9:16/21:9/adaptive
- `--duration` - 视频时长（秒）
- `--draft` - 草稿模式
- `--generate-audio` - 生成音频
- `--api-key` - 覆盖 API Key

### query_task.py

查询任务状态。

```bash
python scripts/query_task.py --help
```

主要参数：
- `task_id` - 任务 ID
- `--watch` - 轮询直到完成
- `--poll-interval` - 轮询间隔（默认 5 秒）
- `--download` - 自动下载视频
- `--json` - JSON 格式输出

### list_tasks.py

列出任务（支持筛选和分页）。

```bash
python scripts/list_tasks.py --help
```

主要参数：
- `--status` - 按状态筛选
- `--model` - 按模型筛选
- `--task-ids` - 特定任务 ID
- `--page-num` - 页码
- `--page-size` - 每页数量

### cancel_task.py

取消或删除任务。

```bash
python scripts/cancel_task.py --help
```

主要参数：
- `task_id` - 任务 ID
- `--api-key` - 覆盖 API Key

## 图像要求

- **支持格式**：JPEG, PNG, WebP, BMP, TIFF, GIF, HEIC/HEIF（仅 1.5 Pro）
- **文件大小**：< 30 MB
- **分辨率**：300-6000 像素
- **宽高比**：0.4 - 2.5

## 任务状态

| 状态 | 描述 |
|------|------|
| queued | 等待处理 |
| running | 正在处理 |
| succeeded | 处理成功 |
| failed | 处理失败 |
| expired | 任务超时 |
| cancelled | 已取消 |

## 注意事项

- 生成的视频 URL 有效期为 **24 小时**，请及时下载
- 文本提示词长度限制为 **500 字符**
- 使用 flex 服务模式（`--service-tier flex`）可以降低 50% 成本，但响应较慢

## 文档

- [API 快速参考](references/api_summary.md)
- [模型详细说明](references/models.md)
- [文生视频示例](examples/text_to_video.md)
- [图生视频示例](examples/image_to_video.md)

## 项目结构

```
seedance-video-generation-skill/
├── SKILL.md                      # Claude Code skill 主文件
├── README.md                     # 项目说明
├── scripts/                      # Python 脚本
│   ├── requirements.txt            # 依赖
│   ├── seedance_client.py          # 核心 API 客户端
│   ├── create_task.py              # 创建任务
│   ├── query_task.py               # 查询任务
│   ├── list_tasks.py               # 列出任务
│   └── cancel_task.py              # 取消任务
├── references/                    # 参考文档
│   ├── api_summary.md             # API 说明
│   └── models.md                  # 模型说明
└── examples/                     # 使用示例
    ├── text_to_video.md           # 文生视频
    └── image_to_video.md          # 图生视频
```

## 许可证

MIT License

## 链接

- [Volcengine Seedance API 文档](https://www.volcengine.com/docs/ark/seedance-video)
- [Volcengine 控制台](https://console.volcengine.com/ark)
- [GitHub 仓库](https://github.com/zBlackIf/seedance-video-generation-skill)

---
name: seedance-video-generation
description: 使用 Volcengine Seedance API 从文本或图像生成视频。支持文生视频、图生视频、草稿到最终视频生成，以及视频生成任务管理。
---

# Seedance Video Generation Skill

使用 Volcengine Seedance API 从文本或图像生成视频的 Claude Code skill。

## Quick Start

### 文生视频（Text-to-Video）

```bash
# 基本文生视频
python scripts/create_task.py --prompt "一只可爱的小猫在阳光下打哈欠"

# 查询任务状态
python scripts/query_task.py --watch <task_id>
```

### 图生视频（Image-to-Video）

```bash
# 单帧图生视频
python scripts/create_task.py --prompt "镜头缓慢拉远展示全景" --image /path/to/image.jpg

# 首尾帧模式
python scripts/create_task.py --prompt "平滑过渡" --image first.jpg --last-frame last.jpg
```

## Authentication

Seedance API 使用 Bearer Token 认证。API Key 获取方式：
1. 访问 [Volcengine 控制台](https://console.volcengine.com/ark)
2. 创建或获取 API Key

设置 API Key（推荐使用环境变量）：
```bash
export ARK_API_KEY="your-api-key-here"
```

或在当前目录创建 `.env` 文件：
```
ARK_API_KEY=your-api-key-here
```

所有脚本也支持 `--api-key` 参数临时覆盖。

## Available Models

| 模型 ID | 类型 | 能力 | 分辨率 | 时长 |
|---------|------|------||--------|------|
| doubao-seedance-1-5-pro-251215 | Pro (最新) | T.2V + I2V + 音频 + 草稿 | 最高 1080p | 2-12s/自动 |
| doubao-seedance-1-0-pro-t2v | Pro | T2V | 最高 1080p | 2-12s |
| doubao-seedance-1-0-pro-i2v | Pro | I2V（首帧+首尾帧） | 最高 1080p | 2-12s |
| doubao-seedance-1-0-pro-fast-t2v | Fast | T2V（快速） | 最高 1080p | 2-12s |
| doubao-seedance-1-0-lite-t2v | Lite | T2V | 最高 720p | 2-12s |
| doubao-seedance-1-0-lite-i2v | Lite | I2V（首帧+首尾帧+参考图） | 最高 720p | 2-12s |

## Text-to-Video Workflow

### 基本用法

```bash
# 使用默认参数生成视频
python scripts/create_task.py --prompt "海边日落，电影感"
```

### 自定义参数

```bash
python scripts/create_task.py \
  --prompt "无人机飞跃山脉" \
  --model doubao-seedance-1-5-pro-251215 \
  --resolution 1080p \
  --ratio 21:9 \
  --duration 8 \
  --seed 12345 \
  --watermark false
```

### 生成带音频的视频（Seedance 1.5 pro）

```bash
python scripts/create_task.py \
  --prompt "厨师在繁忙的餐厅中烹饪，厨师说：'菜好了！'" \
  --generate-audio true
```

### 使用草稿模式

```bash
# 生成快速预览（480p，更快）
python scripts/create_task.py --prompt "测试场景" --draft true

# 获取草稿任务 ID 后，基于草稿生成高质量最终视频
python scripts/create_task.py --draft-task-id <draft_task_id>
```

## Image-to-Video Workflow

### 单帧图生视频

```bash
python scripts/create_task.py \
  --prompt "镜头缓慢拉远，展示完整场景" \
  --image /path/to/image.jpg
```

### 首尾帧模式（首尾帧动画）

```bash
python scripts/create_task.py \
  --prompt "平滑过渡到目标画面" \
  --image /path/to/first_frame.jpg \
  --last-frame /path/to/last_frame.jpg
```

### 参考图像模式（Seedance 1.0 lite i2v）

```bash
# 使用 1-4 张参考图像
python scripts/create_task.py \
  --prompt "[图1]一个人戴着[图2]红色帽子" \
  --reference-images ref1.jpg,ref2.jpg
```

## Task Management

### 查询任务状态

```bash
# 查询单个任务
python scripts/query_task.py <task_id>

# 轮询直到完成（自动显示进度）
python scripts/query_task.py --watch <task_id>

# 自定义轮询间隔
python scripts/query_task.py --watch <task_id> --poll-interval 10

# JSON 格式输出
python scripts/query_task.py --json <task_id>

# 完成后自动下载
python scripts/query_task.py --watch <task_id> --download ./output.mp4
```

### 列出任务

```bash
# 列出所有任务
python scripts/list_tasks.py

# 按状态筛选
python scripts/list_tasks.py --status succeeded

# 按模型筛选
python scripts/list_tasks.py --model doubao-seedance-1-5-pro-251215

# 分页查询
python scripts/list_tasks.py --page-num 1 --page-size 20
```

### 取消/删除任务

```bash
# 取消队列中的任务或删除已完成/失败的任务
python scripts/cancel_task.py <task_id>
```

## Advanced Parameters

### 通用参数

| 参数 | 描述 | 可选值 | 默认值 |
|------|------|--------|--------|
| `--model` | 模型 ID | 见上方模型表 | doubao-seedance-1-5-pro-251215 |
| `--resolution` | 视频分辨率 | 480p, 720p, 1080p | 720p |
| `--ratio` | 宽高比 | 16:9, 4:3, 1:1, 3:4, 9:16, 21:9, adaptive | 16:9 |
| `--duration` | 视频时长（秒） | 2-12 或 -1（自动） | 5 |
| `--seed` | 随机种子 | 任意整数 | 随机 |
| `--watermark` | 是否添加水印 | true, false | false |
| `--api-key` | API Key | 字符串 | 从环境读取 |

### 高级参数

| 参数 | 描述 | 可选值 | 适用模型 |
|------|------|--------|----------|
| `--camera-fixed` | 固定相机位置 | true, false | 所有模型 |
| `--generate-audio` | 生成音频 | true, false | Seedance 1.5 pro |
| `--draft` | 生成草稿预览 | true, false | Seedance 1.5 pro |
| `--draft-task-id` | 基于草稿生成 | 任务 ID | Seedance 1.5 pro |
| `--service-tier` | 处理模式 | default, flex | 所有模型 |
| `--return-last-frame` | 返回最后一帧 | true, false | 所有模型 |

### 服务模式说明

- `default`：在线模式，响应快，RPM 限制较低
- `flex`：离线模式，TPD 更高，价格降低 50%，响应较慢

### 图像要求

- **支持格式**：JPEG, PNG, WebP, BMP, TIFF, GIF, HEIC/HEIF（仅 Seedance 1.5 pro）
- **文件大小**：< 30 MB
- **分辨率**：300-6000 像素
- **宽高比**：0.4 - 2.5

## Task Status

任务可能的状态：

| 状态 | 描述 |
|------|------|
| `queued` | 等待处理 |
| `running` | 正在处理 |
| `succeeded` | 处理成功 |
| `failed` | 处理失败 |
| `expired` | 任务超时 |
| `cancelled` | 已取消 |

## Error Handling

### 常见错误

**API Key 错误**
```
AuthenticationError: Invalid API Key
```
解决：检查 `VOLCENGINE_API_KEY` 环境变量或使用 `--api-key` 参数

**参数错误**
```
InvalidRequestError: Invalid parameter value
```
解决：检查参数值是否符合模型要求

**任务未找到**
```
TaskNotFoundError: Task not found
```
解决：检查任务 ID 是否正确

**限流错误**
```
RateLimitError: Rate limit exceeded
```
解决：等待一段时间后重试，或使用 flex 服务模式

### 输出视频有效期

生成的视频 URL 有效期为 24 小时，请及时下载。

## Additional Resources

- [API 详细文档](references/api_summary.md)
- [模型说明](references/models.md)
- [文生视频示例](examples/text_to_video.md)
- [图生视频示例](examples/image_to_video.md)

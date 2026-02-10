# Seedance API 快速参考

## Base URL
```
https://ark.cn-beijing.volces.com/api/v3
```

## Authentication
```
Authorization: Bearer $ARK_API_KEY
```

---

## 1. 创建视频生成任务

**Endpoint:** `POST /contents/generations/tasks`

**请求示例 (文生视频):**
```json
{
  "model": "doubao-seedance-1-5-pro-251215",
  "content": [
    {
      "type": "text",
      "text": "一只可爱的小猫在阳光下打哈欠"
    }
  ],
  "resolution": "720p",
  "ratio": "16:9",
  "duration": 5,
  "watermark": false
}
```

**请求示例 (图生视频 - 单帧):**
```json
{
  "model": "doubao-seedance-1-0-pro-i2v",
  "content": [
    {
      "type": "text",
      "text": "镜头缓慢拉远展示全景"
    },
    {
      "type": "image",
      "image_url": "data:image/jpeg;base64,...",
      "role": "first_frame"
    }
  ],
  "resolution": "720p",
  "ratio": "16:9",
  "duration": 5
}
```

**请求示例 (图生视频 - 首尾帧):**
```json
{
  "model": "doubao-seedance-1-0-pro-i2v",
  "content": [
    {
      "type": "text",
      "text": "平滑过渡到目标画面"
    },
    {
      "type": "image",
      "image_url": "data:image/jpeg;base64,...",
      "role": "first_frame"
    },
    {
      "type": "image",
      "image_url": "data:image/jpeg;base64,...",
      "role": "last_frame"
    }
  ],
  "resolution": "720p",
  "ratio": "16:9",
  "duration": 5
}
```

**请求示例 (草稿转最终视频):**
```json
{
  "model": "doubao-seedance-1-5-pro-251215",
  "content": [
    {
      "type": "draft_task",
      "draft_task_id": "abc123..."
    }
  ],
  "watermark": false
}
```

**响应示例:**
```json
{
  "id": "task_id_here",
  "status": "queued",
  "model": "doubao-seedance-1-5-pro-251215",
  "created_at": "2024-01-01T12:00:00Z"
}
```

---

## 2. 查询任务状态

**Endpoint:** `GET /contents/generations/tasks/{id}`

**响应示例 (进行中):**
```json
{
  "id": "task_id_here",
  "status": "running",
  "model": "doubao-seedance-1-5-pro-251215",
  "created_at": "2024-01-01T12:00:00Z"
}
```

**响应示例 (成功):**
```json
{
  "id": "task_id_here",
  "status": "succeeded",
  "model": "doubao-seedance-1-5-pro-251215",
  "created_at": "2024-01-01T12:00:00Z",
  "completed_at": "2024-01-01T12:05:00Z",
  "content": {
    "video_url": "https://...",
    "last_frame_url": "https://..."
  },
  "resolution": "720p",
  "ratio": "16:9",
  "duration": 5,
  "usage": {
    "input_tokens": 100,
    "output_tokens": 2000
  }
}
```

**响应示例 (失败):**
```json
{
  "id": "task_id_here",
  "status": "failed",
  "model": "doubao-seedance-1-5-pro-251215",
  "created_at": "2024-01-01T12:00:00Z",
  "completed_at": "2024-01-01T12:01:00Z",
  "error_message": "Internal error"
}
```

---

## 3. 列出任务

**Endpoint:** `GET /contents/generations/tasks?page_num=1&page_size=10&filter.status=succeeded`

**查询参数:**
- `page_num`: 页码（从 1 开始）
- `page_size`: 每页数量（最大 500）
- `filter.status`: 按状态筛选
- `filter.model`: 按模型筛选
- `filter.task_ids`: 特定任务 ID（逗号分隔）

**响应示例:**
```json
{
  "tasks": [
    {
      "id": "task_id_1",
      "status": "succeeded",
      "model": "doubao-seedance-1-5-pro-251215",
      "created": "2024-01-01T12:00:00Z",
      "completed": "2024-01-01T12:05:00Z"
    },
    {
      "id": "task_id_2",
      "status": "running",
      "model": "doubao-seedance-1-5-pro-251215",
      "created": "2024-01-01T12:10:00Z"
    }
  ],
  "page": {
    "page_num": 1,
    "page_size": 10,
    "total": 25
  }
}
```

---

## 4. 取消/删除任务

**Endpoint:** `DELETE /contents/generations/tasks/{id}`

**响应示例:**
```json
{
  "message": "Task cancelled"
}
```

---

## 任务状态

| 状态 | 描述 |
|------|------|
| `queued` | 等待处理 |
| `running` | 正在处理 |
| `succeeded` | 处理成功 |
| `failed` | 处理失败 |
| `expired` | 任务超时 |
| `cancelled` | 已取消 |

---

## 常见错误码

| 状态码 | 说明 |
|--------|------|
| 400 | 请求参数错误 |
| 401 | API Key 无效 |
| 404 | 任务不存在 |
| 429 | 限流 |
| 500+ | 服务器错误 |

---

## 注意事项

1. **视频 URL 有效期**: 生成的视频 URL 有效期为 24 小时
2. **图像文件要求**:
   - 支持格式：JPEG, PNG, WebP, BMP, TIFF, GIF, HEIC/HEIF（仅 Seedance 1.5 pro）
   - 文件大小：< 30 MB
   - 分辨率：300-6000 像素
   - 宽高比：0.4 - 2.5
3. **文本提示词长度**: 最多 500 字符

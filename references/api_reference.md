# Seedance API Reference

Complete reference documentation for Volcengine Seedance Video Generation API.

## Base URLs

- **Data Plane API**: `https://ark.cn-beijing.volces.com/api/v3`
- **Control Plane API**: `https://ark.cn-beijing.volcengineapi.com/`

## Authentication

### API Key Authentication (Recommended)

Use API Key in the Authorization header:

```bash
Authorization: Bearer $ARK_API_KEY
```

### Environment Variable Configuration

Set your API key as an environment variable:

```bash
export ARK_API_KEY="your-api-key-here"
```

---

## Create Video Generation Task

### Endpoint

```
POST https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks
```

### Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `model` | string | Yes | Model ID (e.g., `doubao-seedance-1-5-pro-251215`) |
| `content` | array | Yes | Array of content objects (text/image/video) |
| `callback_url` | string | No | Callback URL for task status updates |
| `return_last_frame` | boolean | No | Return last frame image (default: false) |
| `service_tier` | string | No | Service tier: `default` (online) or `flex` (offline, 50% cost) |
| `execution_expires_after` | integer | No | Task timeout in seconds (default: 172800, range: [3600, 259200]) |
| `generate_audio` | boolean | No | Generate audio (default: true, 1.5 pro only) |
| `draft` | boolean | No | Enable draft mode (default: false, 1.5 pro only) |
| `resolution` | string | No | Video resolution: `480p`, `720p`, `1080p` |
| `ratio` | string | No | Aspect ratio: `16:9`, `4:3`, `1:1`, `3:4`, `9:16`, `21:9`, `adaptive` |
| `duration` | integer | No | Video duration in seconds (2-12, default: 5) |
| `frames` | integer | No | Number of frames (alternative to duration, 1.5 pro not supported) |
| `seed` | integer | No | Seed for reproducibility (default: -1, range: [-1, 2^32-1]) |
| `camera_fixed` | boolean | No | Fix camera (default: false, reference image not supported) |
| `watermark` | boolean | No | Add watermark (default: false) |

### Content Types

#### Text Content

```json
{
  "type": "text",
  "text": "小猫对着镜头打哈欠"
}
```

#### Image Content (URL)

```json
{
  "type": "image_url",
  "image_url": {
    "url": "https://example.com/image.jpg"
  }
}
```

#### Image Content (Base64)

```json
{
  "type": "image_url",
  "image_url": {
    "url": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD..."
  }
}
```

#### Image Content with Role

```json
{
  "type": "image_url",
  "image_url": {
    "url": "data:image/jpeg;base64,...",
    "role": "first_frame"
  }
}
```

Image roles:
- `first_frame`: First frame image
- `last_frame`: Last frame image (for首尾帧 generation)
- `reference_image`: Reference image (1-4 images, 1.0 lite i2v only)

### Response

```json
{
  "id": "cgt-20250331175019-68d9t"
}
```

---

## Query Video Generation Task

### Endpoint

```
GET https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks/{id}
```

### Response Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | string | Task ID |
| `model` | string | Model name and version |
| `status` | string | Task status: `queued`, `running`, `cancelled`, `succeeded`, `failed`, `expired` |
| `error` | object/null | Error information (null on success) |
| `error.code` | string | Error code |
| `error.message` | string | Error message |
| `created_at` | integer | Creation timestamp (Unix seconds) |
| `updated_at` | integer | Last update timestamp (Unix seconds) |
| `content.video_url` | string | Generated video URL (valid for 24 hours) |
| `content.last_frame_url` | string | Last frame image URL (if `return_last_frame: true`) |
| `seed` | integer | Seed value used |
| `resolution` | string | Video resolution |
| `ratio` | string | Aspect ratio |
| `duration` | integer | Video duration in seconds |
| `frames` | integer | Number of frames |
| `framespersecond` | integer | Frame rate |
| `generate_audio` | boolean | Whether audio was generated |
| `draft` | boolean | Whether this is a draft video |
| `draft_task_id` | string | Draft task ID (if generated from draft) |
| `service_tier` | string | Service tier used |
| `execution_expires_after` | integer | Task timeout threshold |
| `usage.completion_tokens` | integer | Tokens used for output |
| `usage.total_tokens` | integer | Total tokens used |

---

## List Video Generation Tasks

### Endpoint

```
GET https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks?page_num={page_num}&page_size={page_size}&filter.status={filter.status}&filter.task_ids={filter.task_ids}&filter.model={filter.model}
```

### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `page_num` | integer | Page number (1-500) |
| `page_size` | integer | Items per page (1-500) |
| `filter.status` | string | Filter by status: `queued`, `running`, `cancelled`, `succeeded`, `failed`, `expired` |
| `filter.task_ids` | array | Filter by task IDs |
| `filter.model` | string | Filter by model/endpoint ID |
| `filter.service_tier` | string | Filter by service tier: `default`, `flex` |

### Response

```json
{
  "items": [
    {
      "id": "cgt-20250331175019-68d9t",
      "model": "doubao-seedance-1-5-pro-251215",
      "status": "succeeded",
      ...
    }
  ],
  "total": 10
}
```

---

## Delete Video Generation Task

### Endpoint

```
DELETE https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks/{id}
```

### Operation by Status

| Status | DELETE Supported | Operation | Result |
|---------|-----------------|------------|---------|
| queued | Yes | Cancel task | cancelled |
| running | No | - | - |
| succeeded | Yes | Delete record | Record removed |
| failed | Yes | Delete record | Record removed |
| cancelled | No | - | - |
| expired | Yes | Delete record | Record removed |

---

## Supported Models

| Model ID | Type | Features |
|----------|------|----------|
| `doubao-seedance-1-5-pro-251215` | Pro | Text-to-video, Image-to-video (first/last frame), Audio generation, Draft mode, Adaptive ratio |
| `doubao-seedance-1-0-pro-251215` | Pro | Text-to-video, Image-to-video (first/last frame) |
| `doubao-seedance-1-0-lite-t2v-251215` | Lite | Text-to-video |
| `doubao-seedance-1-0-lite-i2v-251215` | Lite | Image-to-video (reference image 1-4, first/last frame) |

### Resolution vs Aspect Ratio (Seedance 1.5 Pro)

| Resolution | Ratio | Width x Height |
|-----------|--------|----------------|
| 480p | 16:9 | 864×496 |
| 480p | 4:3 | 752×560 |
| 480p | 1:1 | 640×640 |
| 480p | 3:4 | 560×752 |
| 480p | 9:16 | 496×864 |
| 480p | 21:9 | 992×432 |
| 720p | 16:9 | 1280×720 |
| 720p | 4:3 | 1112×834 |
| 720p | 1:1 | 960×960 |
| 720p | 3:4 | 834×1112 |
| 720p | 9:16 | 720×1280 |
| 720p | 21:9 | 1470×630 |
| 1080p | 16:9 | 1920×1080 |
| 1080p | 4:3 | 1664×1248 |
| 1080p | 1:1 | 1440×1440 |
| 1080p | 3:4 | 1248×1664 |
| 1080p | 9:16 | 1080×1920 |
| 1080p | 21:9 | 2206×946 |

### Supported Image Formats

- jpeg, jpg, png, webp, bmp, tiff, gif
- heic, heif (1.5 pro only)

### Image Requirements

- Aspect ratio: (0.4, 2.5)
- Dimensions: 300-6000 pixels
- Size: < 30 MB

---

## Rate Limits

### Service Tier: Default (Online)

Lower RPM and concurrency limits. Suitable for real-time use.

### Service Tier: Flex (Offline)

Higher TPD limits, 50% cost. Suitable for batch processing.

---

## Task Lifecycle

```
queued → running → succeeded
               ↓
             failed
               ↓
             expired
               ↓
             cancelled
```

---

## Error Codes

Common error codes and their meanings:

| Code | Description |
|-------|-------------|
| `InvalidParameter` | Invalid request parameter |
| `InvalidModel` | Model not found or not authorized |
| `InvalidApiKey` | API key is invalid or expired |
| `InsufficientBalance` | Insufficient account balance |
| `RateLimitExceeded` | Rate limit exceeded |
| `TaskNotFound` | Task not found or expired |
| `ImageInvalid` | Invalid image format or size |
| `InternalError` | Internal server error |

---

## SDK Installation

### Python

```bash
pip install 'volcengine-python-sdk[ark]'
```

### Go

```bash
go get -u github.com/volcengine/volcengine-go-sdk
```

### Java

Add to `pom.xml`:

```xml
<dependency>
  <groupId>com.volcengine</groupId>
  <artifactId>volcengine-java-sdk-ark-runtime</artifactId>
  <version>LATEST</version>
</dependency>
```

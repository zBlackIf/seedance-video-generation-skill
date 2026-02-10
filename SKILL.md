---
name: seedance-video-generation
description: Generate videos using Volcengine Seedance API. Supports text-to-video and image-to-video generation. Use when user asks to: generate video from text description/prompt, create video from image, make video with specific visual content, or produce video content from text or image input.
---

# Seedance Video Generation

Generate videos using Volcengine Seedance API. Supports text-to-video and image-to-video generation.

## Quick Start

```bash
# Text to video
python scripts/seedance.py text-to-video --text "description" --duration 5

# Image to video
python scripts/seedance.py image-to-video --image "/path/to/image.jpg" --duration 5

# Query task status
python scripts/seedance.py query --task-id <task-id>
```

## Commands

### text-to-video

Generate video from text prompt.

**Required:** `--text` - Text prompt for video generation

**Optional parameters:**
- `--duration` - Duration in seconds (2-12, default: 5)
- `--resolution` - Resolution: 480p, 720p, 1080p
- `--ratio` - Aspect ratio: 16:9, 4:3, 1:1, 3:4, 9:16, 21:9, adaptive
- `--model` - Model ID (default: doubao-seedance-1-5-pro-251215)
- `--seed` - Seed for reproducibility (-1 for random)
- `--watermark` - Add watermark
- `--draft` - Enable draft mode (1.5 pro, lower cost)
- `--generate-audio` - Generate audio (1.5 pro)
- `--async` - Return task ID immediately without polling

### image-to-video

Generate video from image.

**Required:** `--image` - Image URL, base64, or file path

**Optional parameters:**
- `--text` - Text prompt to guide generation
- `--duration` - Duration in seconds (2-12, default: 5)
- `--resolution` - Resolution: 480p, 720p, 1080p
- `--ratio` - Aspect ratio: 16:9, 4:3, 1:1, 3:4, 9:16, 21:9, adaptive
- `--model` - Model ID (default: doubao-seedance-1-5-pro-251215)
- `--seed` - Seed for reproducibility (-1 for random)
- `--watermark` - Add watermark
- `--draft` - Enable draft mode (1.5 pro)
- `--generate-audio` - Generate audio (1.5 pro)
- `--async` - Return task ID immediately without polling

### query

Query video generation task status.

**Required:** `--task-id` - Task ID to query

**Optional:** `--follow` - Poll until task completes

## Configuration

API key is required. Configure via:
- `~/.config/seedance/config.json` (see `config/seedance.json.example`)
- Environment variable: `ARK_API_KEY`

## Additional Documentation

- **API Reference**: [references/api_reference.md](references/api_reference.md) - Complete API parameters, models, error codes, and content types

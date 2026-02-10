# 图生视频示例

## 单帧图生视频

```bash
python scripts/create_task.py \
  --prompt "镜头缓慢拉远，展示完整场景" \
  --image /path/to/image.jpg
```

## 首尾帧模式（首尾帧动画）

```bash
python scripts/create_task.py \
  --prompt "平滑过渡到目标画面" \
  --image /path/to/first_frame.jpg \
  --last-frame /path/to/last_frame.jpg
```

## 使用 URL 作为图像输入

```bash
python scripts/create_task.py \
  --prompt "让静态图像动起来" \
  --image https://example.com/image.jpg
```

## 参考图像模式（仅 Seedance 1.0 Lite I2V）

```bash
# 使用 1 张参考图像
python scripts/create_task.py \
  --model doubao-seedance-1-0-lite-i2v \
  --prompt "[图1]一只猫在草地上玩耍" \
  --reference-images /path/to/cat.jpg
```

```bash
# 使用多张参考图像（最多 4 张）
python scripts/create_task.py \
  --model doubao-seedance-1-0-lite-i2v \
  --prompt "[图1]一个人戴着[图2]红色帽子，站在[图3]海边，背景是[图4]夕阳" \
  --reference-images person.jpg,hat.jpg,beach.jpg,sunset.jpg
```

## 自定义参数的图生视频

```bash
python scripts/create_task.py \
  --prompt "电影感的镜头运动" \
  --model doubao-seedance-1-0-pro-i2v \
  --image /path/to/image.jpg \
  --resolution 1080p \
  --ratio 21:9 \
  --duration 8
```

## 首尾帧模式完整示例

```bash
python scripts/create_task.py \
  --prompt "从白天到夜晚的平滑过渡" \
  --model doubao-seedance-1-5-pro-251215 \
  --image /path/to/day_scene.jpg \
  --last-frame /path/to/night_scene.jpg \
  --resolution 1080p \
  --duration 10
```

## 固定相机模式（减少相机运动）

```bash
python scripts/create_task.py \
  --prompt "让人物自然动作" \
  --image /path/to/portrait.jpg \
  --camera-fixed true
```

## 获取最后一帧（用于连续视频生成）

```bash
# 创建任务并获取最后一帧
python scripts/create_task.py \
  --prompt "第一段视频内容" \
  --model doubao-seedance-1-5-pro-251215 \
  --return-last-frame true

# 查询任务获取 last_frame_url
python scripts/query_task.py --json <task_id>

# 使用最后一帧作为下一段视频的首帧
python scripts/create_task.py \
  --prompt "第二段视频内容" \
  --model doubao-seedance-1-5-pro-251215 \
  --image <last_frame_url>
```

## 图像风格迁移

```bash
python scripts/create_task.py \
  --prompt "油画风格的动画效果" \
  --model doubao-seedance-1-0-lite-i2v \
  --reference-images /path/to/style_reference.jpg
```

## 表情动画化

```bash
python scripts/create_task.py \
  --prompt "让微笑的人说话"（带语音提示词用于音频生成） \
  --model doubao-seedance-1-5-pro-251215 \
  --image /path/to/smiling_person.jpg \
  --generate-audio true
```

## 景深和相机运动效果

```bash
python scripts/create_task.py \
  --prompt "缓慢的推镜头，突出主体" \
  --model doubao-seedance-1-0-pro-i2v \
  --image /path/to/product.jpg \
  --ratio 16:9
```

## 完整工作流示例

```bash
# 1. 创建图生视频任务
python scripts/create_task.py \
  --prompt "让静态照片动起来" \
  --image /path/to/photo.jpg

# 输出: Task ID: abc123...

# 2. 轮询等待完成
python scripts/query_task.py --watch abc123...

# 3. 下载生成的视频
python scripts/query_task.py --json abc123... | jq -r '.video_url' | xargs wget -O output.mp4
```

## 图像转 GIF 动画风格

```bash
python scripts/create_task.py \
  --prompt "循环播放的波浪效果" \
  --model doubao-seedance-1-0-lite-i2v \
  --image /path/to/wave.jpg \
  --duration 3
```

## 批量处理多张图像

```bash
#!/bin/bash
# 批量处理脚本

for image in /path/to/images/*.jpg; do
  echo "Processing $image..."
  task_id=$(python scripts/create_task.py \
    --prompt "让图片动起来" \
    --image "$image" \
    --json | jq -r '.id')

  echo "Task ID: $task_id"
done
```

## 图像格式支持

支持的图像格式：
- JPEG
- PNG
- WebP
- BMP
- TIFF
- GIF
- HEIC/HEIF（仅 Seedance 1.5 Pro）

图像要求：
- 文件大小 < 30 MB
- 分辨率 300-6000 像素
- 宽高比 0.4-2.5

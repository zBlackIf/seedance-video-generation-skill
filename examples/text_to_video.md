# 文生视频示例

## 基本文生视频

```bash
python scripts/create_task.py --prompt "一只可爱的小猫在阳光下打哈欠"
```

## 自定义参数

```bash
python scripts/create_task.py \
  --prompt "海边日落，电影感拍摄" \
  --model doubao-seedance-1-5-pro-251215 \
  --resolution 1080p \
  --ratio 21:9 \
  --duration 8 \
  --watermark false
```

## 使用随机种子（用于可复现结果）

```bash
python scripts/create_task.py \
  --prompt "无人机飞跃山脉" \
  --seed 12345
```

## 垂直视频（9:16）

```bash
python scripts/create_task.py \
  --prompt "美食特写镜头" \
  --ratio 9:16
```

## 方形视频（1:1）

```bash
python scripts/create_task.py \
  --prompt "产品展示" \
  --ratio 1:1
```

## 自动时长（Seedance 1.5 Pro）

```bash
python scripts/create_task.py \
  --prompt "一个完整的故事情节" \
  --model doubao-seedance-1-5-pro-251215 \
  --duration -1
```

## 自适应宽高比（Seedance 1.5 Pro）

```bash
python scripts/create_task.py \
  --prompt "竖屏手机视角的短视频内容" \
  --model doubao-seedance-1-5-pro-251215 \
  --ratio adaptive
```

## 带音频生成（Seedance 1.5 Pro）

```bash
python scripts/create_task.py \
  --prompt "厨师在繁忙的餐厅中烹饪，厨师说：'菜好了！'" \
  --model doubao-seedance-1-5-pro-251215 \
  --generate-audio true
```

## 使用草稿模式快速预览（Seedance 1.5 Pro）

```bash
# 步骤 1: 生成草稿（480p，更快）
python scripts/create_task.py \
  --prompt "测试不同的拍摄角度和风格" \
  --model doubao-seedance-1-5-pro-251215 \
  --draft true

# 输出示例: Task ID: abc123...
```

## 基于草稿生成最终视频（Seedance 1.5 Pro）

```bash
# 步骤 2: 获取草稿任务 ID，生成高质量最终视频
python scripts/create_task.py \
  --model doubao-seedance-1-5-pro-251215 \
  --draft-task-id abc123... \
  --resolution 1080p \
  --duration 10
```

## 使用 flex 服务模式（降低成本）

```bash
python scripts/create_task.py \
  --prompt "批量测试视频内容" \
  --service-tier flex
```

## 完整工作流示例

```bash
# 1. 创建任务
python scripts/create_task.py --prompt "测试场景"

# 输出: Task ID: xyz789...

# 2. 轮询等待完成并自动下载
python scripts/query_task.py --watch xyz789... --download output.mp4

# 3. 查看所有成功的任务
python scripts/list_tasks.py --status succeeded
```

## 中文提示词示例

```bash
python scripts/create_task.py --prompt "小猫对着镜头打哈欠，超萌"
```

```bash
python scripts/create_task.py --prompt "樱花飘落，唯美风景"
```

```bash
python scripts/create_task.py --prompt "机器人跳舞，科技感"
```

## 英文提示词示例

```bash
python scripts/create_task.py --prompt "A cute kitten yawning in sunlight"
```

```bash
python scripts/create_task.py --prompt "Cinematic drone shot over mountains at sunset"
```

```bash
python scripts/create_task.py --prompt "Slow motion rain on window glass"
```

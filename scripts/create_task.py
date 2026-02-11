#!/usr/bin/env python3
"""
创建视频生成任务

支持文生视频（T2V）和图生视频（I2V）模式。
生成任务后可自动监控并下载视频。
"""

import argparse
import base64
import os
import sys
import mimetypes
from typing import Optional, List, Dict, Any
from pathlib import Path

try:
    from seedance_client import (
        SeedanceClient,
        InvalidRequestError,
        TaskStatus,
        TimeoutError
    )
except ImportError:
    # 添加当前目录到路径
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from seedance_client import (
        SeedanceClient,
        InvalidRequestError,
        TaskStatus,
        TimeoutError
    )


def read_image_file(file_path: str) -> str:
    """
    读取图像文件并返回 Base64 编码的字符串

    Args:
        file_path: 图像文件路径

    Returns:
        Base64 编码的字符串，格式为 "data:mime/type;base64,..."
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Image file not found: {file_path}")

    if not path.is_file():
        raise ValueError(f"Path is not a file: {file_path}")

    # 获取 MIME 类型
    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type is None:
        # 默认为 image/jpeg
        mime_type = "image/jpeg"

    # 检查文件大小（30MB 限制）
    file_size = path.stat().st_size
    if file_size > 30 * 1024 * 1024:
        raise ValueError(f"Image file exceeds 30MB limit: {file_size / 1024 / 1024:.2f}MB")

    # 读取并编码
    with open(file_path, "rb") as f:
        data = base64.b64encode(f.read()).decode("utf-8")

    return f"data:{mime_type};base64,{data}"


def build_content_array(
    prompt: Optional[str],
    image: Optional[str],
    last_frame: Optional[str],
    reference_images: Optional[List[str]],
    draft_task_id: Optional[str]
) -> List[Dict[str, Any]]:
    """
    构建 content 数组

    Args:
        prompt: 文本提示词
        image: 首帧图像路径
        last_frame: 尾帧图像路径
        reference_images: 参考图像路径列表
        draft_task_id: 草稿任务 ID

    Returns:
        content 数组
    """
    content = []

    # 文本提示词
    if prompt:
        if len(prompt) > 500:
            print(f"Warning: Prompt exceeds 500 characters, truncating...")
            prompt = prompt[:500]
        content.append({"type": "text", "text": prompt})

    # 草稿任务
    if draft_task_id:
        content.append({"type": "draft_task", "draft_task_id": draft_task_id})
        return content

    # 图像输入
    if image:
        image_data = read_image_file(image)
        content.append({"type": "image", "image_url": image_data, "role": "first_frame"})

    if last_frame:
        if not image:
            raise ValueError("--last-frame requires --image to be specified")
        image_data = read_image_file(last_frame)
        content.append({"type": "image", "image_url": image_data, "role": "last_frame"})

    if reference_images:
        for ref_image in reference_images:
            image_data = read_image_file(ref_image)
            content.append({"type": "image", "image_url": image_data, "role": "reference_image"})

    return content


def parse_bool(value: str) -> bool:
    """解析布尔值"""
    if value.lower() in ("true", "1", "yes", "y", "on"):
        return True
    elif value.lower() in ("false", "0", "no", "n", "off", ""):
        return False
    raise ValueError(f"Invalid boolean value: {value}")


def get_output_dir(output_dir: Optional[str]) -> Path:
    """
    获取输出目录

    Args:
        output_dir: 指定的输出目录

    Returns:
        Path 对象
    """
    if output_dir:
        path = Path(output_dir)
    else:
        # 默认使用项目根目录下的 output 文件夹
        path = Path(__file__).parent.parent / "output"

    # 创建目录
    path.mkdir(parents=True, exist_ok=True)
    return path


def generate_filename(task_id: str, prompt: Optional[str] = None) -> str:
    """
    生成文件名

    Args:
        task_id: 任务 ID
        prompt: 文本提示词（用于生成文件名）

    Returns:
        文件名
    """
    # 提取任务 ID 的后缀部分
    task_suffix = task_id.split("-")[-1]

    if prompt:
        # 使用提示词的前几个字符作为文件名
        import re
        # 移除特殊字符，只保留中英文、数字、下划线和短横线
        clean_prompt = re.sub(r'[^\w\u4e00-\u9fff-]', '_', prompt[:20])
        return f"{clean_prompt}_{task_suffix}.mp4"

    return f"video_{task_suffix}.mp4"


def download_video(url: str, output_path: Path):
    """
    下载视频文件

    Args:
        url: 视频下载 URL
        output_path: 输出文件路径
    """
    try:
        import requests
        from tqdm import tqdm
    except ImportError:
        import requests
        tqdm = None

    print(f"\n📥 Downloading video to: {output_path}")

    response = requests.get(url, stream=True)
    response.raise_for_status()

    total_size = int(response.headers.get("content-length", 0))

    with open(output_path, "wb") as f:
        if tqdm:
            progress_bar = tqdm(
                total=total_size,
                unit="B",
                unit_scale=True,
                desc="Downloading"
            )
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                progress_bar.update(len(chunk))
            progress_bar.close()
        else:
            downloaded = 0
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                downloaded += len(chunk)
                if total_size > 0:
                    percent = downloaded / total_size * 100
                    print(f"\r{percent:.1f}%", end="", flush=True)
            print()

    file_size_mb = output_path.stat().st_size / 1024 / 1024
    print(f"✅ Video saved: {output_path} ({file_size_mb:.2f} MB)")


def poll_callback(task):
    """轮询回调函数"""
    if task.status == TaskStatus.RUNNING:
        print(f"\r🔄 Running... (Task: {task.id[:8]}...)", end="", flush=True)
    elif task.status == TaskStatus.QUEUED:
        print(f"\r⏳ Queued... (Task: {task.id[:8]}...)", end="", flush=True)


def main():
    parser = argparse.ArgumentParser(
        description="Create a video generation task using Seedance API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Text-to-video
  python create_task.py --prompt "一只可爱的小猫在阳光下打哈欠"

  # Text-to-video with auto-download
  python create_task.py --prompt "一只可爱的小猫在阳光下打哈欠" --auto-download

  # Image-to-video
  python create_task.py --prompt "镜头缓慢拉远" --image cat.jpg

  # First and last frame
  python create_task.py --prompt "平滑过渡" --image first.jpg --last-frame last.jpg

  # With custom parameters
  python create_task.py \\
    --prompt "海边日落，电影感" \\
    --resolution 1080p \\
    --ratio 21:9 \\
    --duration 8

  # Draft mode with auto-download
  python create_task.py --prompt "测试场景" --draft true --auto-download
        """
    )

    # 必选参数（除非使用 draft-task-id）
    parser.add_argument(
        "--prompt",
        type=str,
        help="Text prompt for video generation"
    )

    # 模型参数
    parser.add_argument(
        "--model",
        type=str,
        default="doubao-seedance-1-5-pro-251215",
        help="Model ID (default: doubao-seedance-1-5-pro-251215)"
    )

    # 图像参数
    parser.add_argument(
        "--image",
        type=str,
        help="Path to first frame image (image-to-video)"
    )
    parser.add_argument(
        "--last-frame",
        type=str,
        help="Path to last frame image (首尾帧 mode)"
    )
    parser.add_argument(
        "--reference-images",
        type=str,
        help="Comma-separated paths to reference images (1-4 images)"
    )

    # 输出参数
    parser.add_argument(
        "--resolution",
        type=str,
        choices=["480p", "720p", "1080p"],
        default="720p",
        help="Video resolution (default: 720p)"
    )
    parser.add_argument(
        "--ratio",
        type=str,
        choices=["16:9", "4:3", "1:1", "3:4", "9:16", "21:9", "adaptive"],
        default="16:9",
        help="Aspect ratio (default: 16:9)"
    )
    parser.add_argument(
        "--duration",
        type=int,
        default=5,
        help="Video duration in seconds, 2-12 or -1 for auto (default: 5)"
    )

    # 高级参数
    parser.add_argument(
        "--seed",
        type=int,
        help="Random seed for reproducibility"
    )
    parser.add_argument(
        "--watermark",
        type=str,
        default="false",
        help="Include watermark (true/false, default: false)"
    )
    parser.add_argument(
        "--camera-fixed",
        type=str,
        default="false",
        help="Fix camera position (true/false, default: false)"
    )
    parser.add_argument(
        "--generate-audio",
        type=str,
        default="false",
        help="Generate audio (Seedance 1.5 pro only, true/false, default: false)"
    )
    parser.add_argument(
        "--draft",
        type=str,
        default="false",
        help="Generate draft preview (Seedance 1.5 pro only, true/false, default: false)"
    )
    parser.add_argument(
        "--draft-task-id",
        type=str,
        help="Generate final video from draft task ID"
    )
    parser.add_argument(
        "--service",
        type=str,
        choices=["default", "flex"],
        default="default",
        help="Service tier: default (online) or flex (offline, cheaper)"
    )
    parser.add_argument(
        "--return-last-frame",
        type=str,
        default="false",
        help="Return last frame image (true/false, default: false)"
    )

    # 认证
    parser.add_argument(
        "--api-key",
        type=str,
        help="Override API Key (overrides ARK_API_KEY env variable)"
    )

    # Watch 和下载参数
    parser.add_argument(
        "--watch",
        action="store_true",
        help="Watch task until completion"
    )
    parser.add_argument(
        "--auto-download",
        action="store_true",
        help="Automatically download video after completion (implies --watch)"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        help="Output directory for downloaded videos (default: ./output)"
    )
    parser.add_argument(
        "--poll-interval",
        type=int,
        default=5,
        help="Seconds between polls when watching (default: 5)"
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=600,
        help="Timeout in seconds when watching (default: 600)"
    )

    # 输出格式
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output raw JSON"
    )

    args = parser.parse_args()

    # 验证参数
    if args.draft_task_id:
        if args.prompt or args.image:
            parser.error("--draft-task-id cannot be used with --prompt or --image")
    else:
        if not args.prompt and not args.image:
            parser.error("--prompt or --image is required (unless using --draft-task-id)")

    if args.last_frame and not args.image:
        parser.error("--last-frame requires --image to be specified")

    if args.duration != -1 and (args.duration < 2 or args.duration > 12):
        parser.error("--duration must be between 2 and 12, or -1 for auto")

    # auto-download 意味着 watch
    if args.auto_download:
        args.watch = True

    # 解析参考图像
    reference_images = None
    if args.reference_images:
        reference_images = [p.strip() for p in args.reference_images.split(",")]
        if len(reference_images) > 4:
            parser.error("--reference-images supports maximum 4 images")

    # 构建 content 数组
    try:
        content = build_content_array(
            prompt=args.prompt,
            image=args.image,
            last_frame=args.last_frame,
            reference_images=reference_images,
            draft_task_id=args.draft_task_id
        )
    except Exception as e:
        print(f"Error processing images: {e}", file=sys.stderr)
        sys.exit(1)

    # 构建请求 payload
    payload = {
        "model": args.model,
        "content": content,
        "resolution": args.resolution,
        "ratio": args.ratio,
        "duration": args.duration,
        "watermark": parse_bool(args.watermark),
        "service_tier": args.service,
        "return_last_frame": parse_bool(args.return_last_frame)
    }

    # 添加可选参数
    if args.seed is not None:
        payload["seed"] = args.seed

    if parse_bool(args.camera_fixed):
        payload["camera_fixed"] = True

    if parse_bool(args.generate_audio):
        payload["generate_audio"] = True

    if parse_bool(args.draft):
        payload["draft"] = True

    # 创建客户端并发送请求
    try:
        client = SeedanceClient(api_key=args.api_key)

        # 创建任务
        task = client.create_task(payload)

        # 输出创建结果
        if args.json:
            import json
            result = {
                "id": task.id,
                "status": task.status.value,
                "model": task.model,
                "created_at": task.created_at,
                "resolution": task.resolution,
                "ratio": task.ratio,
                "duration": task.duration
            }
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print("✅ Task created successfully!")
            print(f"   Task ID: {task.id}")
            print(f"   Status: {task.status.value}")
            print(f"   Model: {task.model}")
            print(f"   Created at: {task.created_at}")
            if task.resolution:
                print(f"   Resolution: {task.resolution}")
            if task.ratio:
                print(f"   Ratio: {task.ratio}")
            if task.duration:
                print(f"   Duration: {task.duration}s")

        # Watch 模式
        if args.watch:
            print(f"\n⏱ Watching task: {task.id}")
            print(f"   Poll interval: {args.poll_interval}s, Timeout: {args.timeout}s")
            print()

            task = client.wait_for_completion(
                task_id=task.id,
                poll_interval=args.poll_interval,
                timeout=args.timeout,
                callback=poll_callback
            )

            # 清除进度显示
            print("\r" + " " * 60 + "\r", end="", flush=True)

            # 输出最终状态
            status_emoji = {
                TaskStatus.SUCCEEDED: "✅",
                TaskStatus.FAILED: "❌",
                TaskStatus.EXPIRED: "⏰",
                TaskStatus.CANCELLED: "🚫"
            }
            emoji = status_emoji.get(task.status, "❓")

            print(f"{emoji} Task completed!")
            print(f"   Status: {task.status.value}")
            if task.status == TaskStatus.FAILED and task.error_message:
                print(f"   Error: {task.error_message}")

            # 成功时显示信息
            if task.status == TaskStatus.SUCCEEDED:
                if task.usage:
                    input_tokens = task.usage.get("input_tokens", 0)
                    output_tokens = task.usage.get("output_tokens", 0)
                    print(f"   Usage: {input_tokens} input + {output_tokens} output tokens")

                # 自动下载
                if task.video_url and args.auto_download:
                    output_dir = get_output_dir(args.output_dir)
                    filename = generate_filename(task.id, args.prompt)
                    output_path = output_dir / filename
                    download_video(task.video_url, output_path)
                elif task.video_url:
                    print(f"\n📹 Video URL: {task.video_url}")
                    print("   (URL valid for 24 hours)")

    except InvalidRequestError as e:
        print(f"❌ API Error: {e}", file=sys.stderr)
        if e.response:
            print(f"   Details: {e.response}", file=sys.stderr)
        sys.exit(1)
    except TimeoutError as e:
        print(f"\n⏰ Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

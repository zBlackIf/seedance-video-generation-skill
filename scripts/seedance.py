#!/usr/bin/env python3
"""
Seedance Video Generation Skill

Main script for generating videos using Volcengine Seedance API.

Supports:
- Text-to-video generation
- Image-to-video generation (with URL, base64, or local file)
- Task status query with automatic polling

Usage:
    python seedance.py text-to-video --text "prompt" [options]
    python seedance.py image-to-video --image <url|file|base64> [options]
    python seedance.py query --task-id <id>
"""

import argparse
import base64
import json
import os
import sys
import time
import urllib.request
from pathlib import Path
from typing import Any, Dict, Optional, List

# Add site-packages to path for volcengine SDK
import site
for pkg_path in site.getsitepackages():
    if pkg_path not in sys.path:
        sys.path.insert(0, pkg_path)

try:
    from volcenginesdkarkruntime._client import Ark as VolcengineArk
except ImportError:
    print("Error: volcengine-python-sdk is not installed.")
    print("Install it with: pip install 'volcengine-python-sdk[ark]'")
    sys.exit(1)

from config import Config, get_config


# Default model for text-to-video
DEFAULT_T2V_MODEL = "doubao-seedance-1-5-pro-251215"

# Default model for image-to-video
DEFAULT_I2V_MODEL = "doubao-seedance-1-5-pro-251215"

# Supported video resolutions
RESOLUTIONS = ["480p", "720p", "1080p"]

# Supported aspect ratios
RATIOS = ["16:9", "4:3", "1:1", "3:4", "9:16", "21:9", "adaptive"]


def print_json(data: Any) -> None:
    """Print data as formatted JSON."""
    print(json.dumps(data, ensure_ascii=False, indent=2))


def file_to_base64(file_path: str) -> str:
    """
    Read a file and convert to base64 data URI.

    Args:
        file_path: Path to the image file

    Returns:
        Base64 data URI string
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    # Determine MIME type based on extension
    ext_map = {
        ".jpg": "jpeg",
        ".jpeg": "jpeg",
        ".png": "png",
        ".webp": "webp",
        ".bmp": "bmp",
        ".tiff": "tiff",
        ".tif": "tiff",
        ".gif": "gif",
        ".heic": "heic",
        ".heif": "heif",
    }

    ext = path.suffix.lower()
    mime_type = ext_map.get(ext, "jpeg")

    with open(path, "rb") as f:
        b64_data = base64.b64encode(f.read()).decode("utf-8")

    return f"data:image/{mime_type};base64,{b64_data}"


def process_image_input(image_input: str) -> str:
    """
    Process multiple image input formats to URL or base64 data URI.

    Args:
        image_input: Image input as URL, base64 data URI, or file path

    Returns:
        URL or base64 data URI string
    """
    # Check if it's a URL
    if image_input.startswith(("http://", "https://")):
        return image_input

    # Check if it's already a base64 data URI
    if image_input.startswith("data:image/"):
        return image_input

    # Check if it's a local file
    path = Path(image_input)
    if path.exists():
        return file_to_base64(image_input)

    # Assume it's a raw base64 string
    if len(image_input) > 100 and "/" not in image_input:
        # Likely a raw base64 string
        return f"data:image/jpeg;base64,{image_input}"

    # Try as file path one more time (might be relative path)
    try:
        return file_to_base64(image_input)
    except FileNotFoundError:
        raise ValueError(
            f"Invalid image input: {image_input}. "
            "Must be a URL, base64 data URI, or valid file path."
        )


def build_content_for_t2v(text: str) -> List[Dict[str, Any]]:
    """Build content array for text-to-video."""
    return [{"type": "text", "text": text}]


def build_content_for_i2v(
    image: str, text: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Build content array for image-to-video.

    Args:
        image: Image URL or base64 data URI
        text: Optional text prompt

    Returns:
        Content array for API request
    """
    content = [{"type": "image_url", "image_url": {"url": image}}]

    if text:
        content.insert(0, {"type": "text", "text": text})

    return content


def validate_seed(seed: Optional[int]) -> int:
    """Validate and return seed value."""
    if seed is None:
        return -1  # Default random seed

    if not (-1 <= seed <= (2**32 - 1)):
        raise ValueError(f"Seed must be between -1 and {2**32 - 1}")

    return seed


def create_client(config: Config) -> Any:
    """
    Create an Ark client for Seedance API.

    Args:
        config: Configuration instance

    Returns:
        Ark client instance
    """
    is_valid, error = config.validate()
    if not is_valid:
        raise ValueError(error)

    # Create client with API key
    client = VolcengineArk(
        ak=config.ark_api_key,
        region=config.region,
    )

    return client


def submit_video_generation_request(
    client: Any,
    model: str,
    content: List[Dict[str, Any]],
    **kwargs,
) -> str:
    """
    Submit a video generation request.

    Args:
        client: Ark client instance
        model: Model ID
        content: Content array
        **kwargs: Additional parameters (duration, resolution, ratio, seed, etc.)

    Returns:
        Task ID
    """
    # Build request parameters
    request_params: Dict[str, Any] = {
        "model": model,
        "content": content,
    }

    # Add optional parameters
    optional_params = [
        "duration",
        "resolution",
        "ratio",
        "seed",
        "frames",
        "camera_fixed",
        "watermark",
        "generate_audio",
        "draft",
        "callback_url",
        "return_last_frame",
        "service_tier",
        "execution_expires_after",
    ]

    for param in optional_params:
        if param in kwargs and kwargs[param] is not None:
            request_params[param] = kwargs[param]

    # Submit request using content_generation.create
    try:
        response = client.content_generation.create(
            request=request_params,
        )
        return response.id
    except Exception as e:
        raise RuntimeError(f"Failed to submit video generation request: {e}")


def query_task_status(client: Any, task_id: str) -> Dict[str, Any]:
    """
    Query the status of a video generation task.

    Args:
        client: Ark client instance
        task: Task ID to query

    Returns:
        Task status as dictionary
    """
    try:
        task = client.content_generation.get(task_id)

        # Convert to dictionary-like structure
        result = {
            "id": task.id,
            "model": task.model,
            "status": task.status,
            "created_at": task.created_at,
            "updated_at": task.updated_at,
            "seed": task.seed,
        }

        # Add error if present
        if hasattr(task, "error") and task.error:
            result["error"] = {
                "code": task.error.code if task.error else None,
                "message": task.error.message if task.error else None,
            }

        # Add content if available
        if hasattr(task, "content") and task.content:
            content_dict = {}
            if hasattr(task.content, "video_url") and task.content.video_url:
                content_dict["video_url"] = task.content.video_url
            if (
                hasattr(task.content, "last_frame_url")
                and task.content.last_frame_url
            ):
                content_dict["last_frame_url"] = task.content.last_frame_url
            if content_dict:
                result["content"] = content_dict

        # Add video parameters
        for attr in [
            "resolution",
            "ratio",
            "duration",
            "frames",
            "framespersecond",
            "generate_audio",
            "draft",
            "draft_task_id",
            "service_tier",
            "execution_expires_after",
        ]:
            if hasattr(task, attr):
                result[attr] = getattr(task, attr)

        # Add usage info
        if hasattr(task, "usage") and task.usage:
            result["usage"] = {
                "completion_tokens": task.usage.completion_tokens,
                "total_tokens": task.usage.total_tokens,
            }

        return result

    except Exception as e:
        raise RuntimeError(f"Failed to query task status: {e}")


def poll_task_completion(
    client: Any,
    task_id: str,
    timeout: int = 300,
    poll_interval: int = 5,
    verbose: bool = True,
) -> Dict[str, Any]:
    """
    Poll a task until it completes, fails, or times out.

    Args:
        client: Ark client instance
        task_id: Task ID to poll
        timeout: Maximum time to wait in seconds
        poll_interval: Time between polls in seconds
        verbose: Whether to print status updates

    Returns:
        Final task status as dictionary
    """
    start_time = time.time()

    if verbose:
        print(f"Polling task {task_id}...")

    while True:
        elapsed = time.time() - start_time

        if elapsed > timeout:
            raise TimeoutError(
                f"Task timeout after {timeout} seconds. "
                f"Use --async flag to get just the task ID, "
                f"then query later with: python seedance.py query --task-id {task_id}"
            )

        status = query_task_status(client, task_id)

        if verbose:
            print(f"  Status: {status['status']}", end="\r")
            sys.stdout.flush()

        if status["status"] == "succeeded":
            if verbose:
                print()
                print("Task completed successfully!")
            return status
        elif status["status"] in ("failed", "expired", "cancelled"):
            if verbose:
                print()
            error = status.get("error", {})
            error_msg = error.get("message", "Unknown error")
            raise RuntimeError(f"Task {status['status']}: {error_msg}")

        time.sleep(poll_interval)


def cmd_text_to_video(args: argparse.Namespace) -> None:
    """Handle text-to-video command."""
    # Get configuration
    config = get_config(args.environment)

    # Create client
    client = create_client(config)

    # Validate parameters
    if not args.text:
        print("Error: --text is required for text-to-video")
        sys.exit(1)

    # Validate resolution
    if args.resolution and args.resolution not in RESOLUTIONS:
        print(f"Error: Invalid resolution. Must be one of: {', '.join(RESOLUTIONS)}")
        sys.exit(1)

    # Validate ratio
    if args.ratio and args.ratio not in RATIOS:
        print(f"Error: Invalid ratio. Must be one of: {', '.join(RATIOS)}")
        sys.exit(1)

    # Validate duration
    if args.duration and not (2 <= args.duration <= 12):
        print("Error: Duration must be between 2 and 12 seconds")
        sys.exit(1)

    # Build content
    content = build_content_for_t2v(args.text)

    # Get model
    model = args.model or DEFAULT_T2V_MODEL

    # Build request parameters
    request_kwargs = {
        "duration": args.duration,
        "resolution": args.resolution,
        "ratio": args.ratio,
        "seed": validate_seed(args.seed),
        "camera_fixed": args.camera_fixed,
        "watermark": args.watermark,
        "generate_audio": args.generate_audio,
        "draft": args.draft,
        "return_last_frame": args.return_last_frame,
    }

    if args.frames:
        request_kwargs["frames"] = args.frames

    if args.service_tier:
        request_kwargs["service_tier"] = args.service_tier

    if args.callback_url:
        request_kwargs["callback_url"] = args.callback_url

    # Submit request
    print(f"Submitting text-to-video request with model: {model}")
    task_id = submit_video_generation_request(client, model, content, **request_kwargs)
    print(f"Task ID: {task_id}")

    # Return early if async mode
    if args.async_mode:
        print(f"Query status with: python seedance.py query --task-id {task_id}")
        return

    # Poll for completion
    try:
        timeout = args.timeout or config.timeout
        poll_interval = args.poll_interval or config.poll_interval
        result = poll_task_completion(client, task_id, timeout, poll_interval)

        if "content" in result:
            print(f"Video URL: {result['content'].get('video_url')}")
            if "last_frame_url" in result["content"]:
                print(f"Last Frame URL: {result['content'].get('last_frame_url')}")

        if args.verbose:
            print("\nFull result:")
            print_json(result)

    except TimeoutError as e:
        print(f"\nError: {e}")
        sys.exit(1)
    except RuntimeError as e:
        print(f"\nError: {e}")
        sys.exit(1)


def cmd_image_to_video(args: argparse.Namespace) -> None:
    """Handle image-to-video command."""
    # Get configuration
    config = get_config(args.environment)

    # Create client
    client = create_client(config)

    # Validate parameters
    if not args.image:
        print("Error: --image is required for image-to-video")
        sys.exit(1)

    # Validate resolution
    if args.resolution and args.resolution not in RESOLUTIONS:
        print(f"Error: Invalid resolution. Must be one of: {', '.join(RESOLUTIONS)}")
        sys.exit(1)

    # Validate ratio
    if args.ratio and args.ratio not in RATIOS:
        print(f"Error: Invalid ratio. Must be one of: {', '.join(RATIOS)}")
        sys.exit(1)

    # Validate duration
    if args.duration and not (2 <= args.duration <= 12):
        print("Error: Duration must be between 2 and 12 seconds")
        sys.exit(1)

    # Process image input
    print("Processing image input...")
    image_url = process_image_input(args.image)

    # Build content
    content = build_content_for_i2v(image_url, args.text)

    # Get model
    model = args.model or DEFAULT_I2V_MODEL

    # Build request parameters
    request_kwargs = {
        "duration": args.duration,
        "resolution": args.resolution,
        "ratio": args.ratio,
        "seed": validate_seed(args.seed),
        "camera_fixed": args.camera_fixed,
        "watermark": args.watermark,
        "generate_audio": args.generate_audio,
        "draft": args.draft,
        "return_last_frame": args.return_last_frame,
    }

    if args.frames:
        request_kwargs["frames"] = args.frames

    if args.service_tier:
        request_kwargs["service_tier"] = args.service_tier

    if args.callback_url:
        request_kwargs["callback_url"] = args.callback_url

    # Submit request
    print(f"Submitting image-to-video request with model: {model}")
    task_id = submit_video_generation_request(client, model, content, **request_kwargs)
    print(f"Task ID: {task_id}")

    # Return early if async mode
    if args.async_mode:
        print(f"Query status with: python seedance.py query --task-id {task_id}")
        return

    # Poll for completion
    try:
        timeout = args.timeout or config.timeout
        poll_interval = args.poll_interval or config.poll_interval
        result = poll_task_completion(client, task_id, timeout, poll_interval)

        if "content" in result:
            print(f"Video URL: {result['content'].get('video_url')}")
            if "last_frame_url" in result["content"]:
                print(f"Last Frame URL: {result['content'].get('last_frame_url')}")

        if args.verbose:
            print("\nFull result:")
            print_json(result)

    except TimeoutError as e:
        print(f"\nError: {e}")
        sys.exit(1)
    except RuntimeError as e:
        print(f"\nError: {e}")
        sys.exit(1)


def cmd_query(args: argparse.Namespace) -> None:
    """Handle query command."""
    # Get configuration
    config = get_config(args.environment)

    # Create client
    client = create_client(config)

    # Validate parameters
    if not args.task_id:
        print("Error: --task-id is required for query")
        sys.exit(1)

    # Query task status
    print(f"Querying task: {args.task_id}")
    status = query_task_status(client, args.task_id)

    print_json(status)

    # If task succeeded and follow is enabled, poll for completion
    if args.follow and status["status"] in ("queued", "running"):
        print(f"\nTask is {status['status']}. Polling for completion...")
        try:
            timeout = args.timeout or config.timeout
            poll_interval = args.poll_interval or config.poll_interval
            result = poll_task_completion(
                client, args.task_id, timeout, poll_interval, verbose=True
            )

            if "content" in result:
                print(f"\nVideo URL: {result['content'].get('video_url')}")
                if "last_frame_url" in result["content"]:
                    print(f"Last Frame URL: {result['content'].get('last_frame_url')}")

        except TimeoutError as e:
            print(f"\nError: {e}")
            sys.exit(1)
        except RuntimeError as e:
            print(f"\nError: {e}")
            sys.exit(1)


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Seedance Video Generation - Generate videos using Volcengine Seedance API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Text-to-video (polling mode)
  python seedance.py text-to-video --text "小猫猫" --duration 5 --resolution 720p

  # Text-to-video (async mode)
  python seedance.py text-to-video --text "海浪" --async

  # Text-to-video with specific model
  python seedance.py text-to-video --text "日落" --model doubao-seedance-1-5-pro-251215

  # Image-to-video (URL)
  python seedance.py image-to-video --image "https://example.com/photo.jpg" --duration 5

  # Image-to-video (local file)
  python seedance.py image-to-video --image "/path/to/image.jpg" --duration 5

  # Image-to-video with text prompt
  python seedance.py image-to-video --image "/path/to/image.jpg" --text "夕阳下的海滩" --duration 5

  # Query task status
  python seedance.py query --task-id cgt-20250331175019-68d9t

  # Query and follow until completion
  python seedance.py query --task-id cgt-20250331175019-68d9t --follow
""",
    )

    # Global arguments
    parser.add_argument(
        "-e",
        "--environment",
        default="default",
        help="Configuration environment (default, development, production)",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose output"
    )

    # Timeout and poll interval (global for polling)
    parser.add_argument(
        "--timeout",
        type=int,
        help="Timeout for task polling in seconds (default: from config)",
    )
    parser.add_argument(
        "--poll-interval",
        type=int,
        help="Poll interval in seconds (default: from config)",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # text-to-video command
    t2v_parser = subparsers.add_parser(
        "text-to-video", help="Generate video from text prompt"
    )
    t2v_parser.add_argument(
        "--text", required=True, help="Text prompt for video generation"
    )
    t2v_parser.add_argument(
        "--model", help=f"Model ID (default: {DEFAULT_T2V_MODEL})"
    )
    t2v_parser.add_argument(
        "--duration", type=int, help="Video duration in seconds (2-12, default: 5)"
    )
    t2v_parser.add_argument(
        "--resolution",
        choices=RESOLUTIONS,
        help="Video resolution (default: 720p for 1.5 pro/lite, 1080p for 1.0 pro)",
    )
    t2v_parser.add_argument(
        "--ratio",
        choices=RATIOS,
        help="Aspect ratio (default: adaptive for 1.5 pro, 16:9 for others)",
    )
    t2v_parser.add_argument(
        "--seed", type=int, help="Seed for reproducibility (-1 for random)"
    )
    t2v_parser.add_argument(
        "--frames", type=int, help="Number of frames (alternative to duration)"
    )
    t2v_parser.add_argument(
        "--camera-fixed", type=bool, help="Whether to fix camera (default: false)"
    )
    t2v_parser.add_argument(
        "--watermark", action="store_true", help="Add watermark to video"
    )
    t2v_parser.add_argument(
        "--generate-audio",
        type=bool,
        help="Generate audio (default: true for 1.5 pro)",
    )
    t2v_parser.add_argument(
        "--draft",
        action="store_true",
        help="Enable draft mode (1.5 pro only, lower cost preview)",
    )
    t2v_parser.add_argument(
        "--return-last-frame",
        action="store_true",
        help="Return last frame image",
    )
    t2v_parser.add_argument(
        "--service-tier",
        choices=["default", "flex"],
        help="Service tier (default: online, flex: offline 50% cost)",
    )
    t2v_parser.add_argument(
        "--callback-url", help="Callback URL for task status updates"
    )
    t2v_parser.add_argument(
        "--async",
        dest="async_mode",
        action="store_true",
        help="Return task ID immediately without polling",
    )

    # image-to-video command
    i2v_parser = subparsers.add_parser(
        "image-to-video", help="Generate video from image"
    )
    i2v_parser.add_argument(
        "--image", required=True, help="Image URL, base64, or local file path"
    )
    i2v_parser.add_argument(
        "--text", help="Optional text prompt to guide video generation"
    )
    i2v_parser.add_argument(
        "--model", help=f"Model ID (default: {DEFAULT_I2V_MODEL})"
    )
    i2v_parser.add_argument(
        "--duration", type=int, help="Video duration in seconds (2-12, default: 5)"
    )
    i2v_parser.add_argument(
        "--resolution",
        choices=RESOLUTIONS,
        help="Video resolution (default: 720p for 1.5 pro/lite, 1080p for 1.0 pro)",
    )
    i2v_parser.add_argument(
        "--ratio",
        choices=RATIOS,
        help="Aspect ratio (default: adaptive for first/last frame)",
    )
    i2v_parser.add_argument(
        "--seed", type=int, help="Seed for reproducibility (-1 for random)"
    )
    i2v_parser.add_argument(
        "--frames", type=int, help="Number of frames (alternative to duration)"
    )
    i2v_parser.add_argument(
        "--camera-fixed", type=bool, help="Whether to fix camera (default: false)"
    )
    i2v_parser.add_argument(
        "--watermark", action="store_true", help="Add watermark to video"
    )
    i2v_parser.add_argument(
        "--generate-audio",
        type=bool,
        help="Generate audio (default: true for 1.5 pro)",
    )
    i2v_parser.add_argument(
        "--draft",
        action="store_true",
        help="Enable draft mode (1.5 pro only, lower cost preview)",
    )
    i2v_parser.add_argument(
        "--return-last-frame",
        action="store_true",
        help="Return last frame image",
    )
    i2v_parser.add_argument(
        "--service-tier",
        choices=["default", "flex"],
        help="Service tier (default: online, flex: offline 50% cost)",
    )
    i2v_parser.add_argument(
        "--callback-url", help="Callback URL for task status updates"
    )
    i2v_parser.add_argument(
        "--async",
        dest="async_mode",
        action="store_true",
        help="Return task ID immediately without polling",
    )

    # query command
    query_parser = subparsers.add_parser(
        "query", help="Query video generation task status"
    )
    query_parser.add_argument("--task-id", required=True, help="Task ID to query")
    query_parser.add_argument(
        "--follow",
        action="store_true",
        help="Poll until task completes (if queued or running)",
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        if args.command == "text-to-video":
            cmd_text_to_video(args)
        elif args.command == "image-to-video":
            cmd_image_to_video(args)
        elif args.command == "query":
            cmd_query(args)
        else:
            parser.print_help()
            sys.exit(1)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        if args.verbose:
            import traceback

            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

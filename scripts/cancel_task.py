#!/usr/bin/env python3
"""
取消或删除视频生成任务

取消队列中的任务，或删除已完成/失败的任务记录。
"""

import os
import sys
import argparse

try:
    from seedance_client import SeedanceClient, TaskNotFoundError
except ImportError:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from seedance_client import SeedanceClient, TaskNotFoundError


def main():
    parser = argparse.ArgumentParser(
        description="Cancel or delete a video generation task",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Cancel queued task
  python cancel_task.py <task_id>

  # Delete completed/failed task record
  python cancel_task.py <task_id>
        """
    )

    parser.add_argument(
        "task_id",
        type=str,
        help="Task ID to cancel/delete"
    )
    parser.add_argument(
        "--api-key",
        type=str,
        help="Override API Key"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output raw JSON"
    )

    args = parser.parse_args()

    try:
        client = SeedanceClient(api_key=args.api_key)
        result = client.cancel_task(args.task_id)

        if args.json:
            import json
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(f"Task {args.task_id} cancelled/deleted successfully.")
            if result:
                print(f"Response: {result}")

    except TaskNotFoundError:
        print(f"Error: Task not found: {args.task_id}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

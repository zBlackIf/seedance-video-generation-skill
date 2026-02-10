#!/usr/bin/env python3
"""
列出视频生成任务

支持按状态、模型和任务 ID 筛选，并支持分页。
"""

import os
import sys
import argparse

try:
    from seedance_client import SeedanceClient
except ImportError:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from seedance_client import SeedanceClient


def format_task_list(data: dict) -> str:
    """
    格式化任务列表为易读表格

    Args:
        data: API 返回的数据

    Returns:
        格式化的字符串
    """
    tasks = data.get("tasks", [])
    page_info = data.get("page", {})

    if not tasks:
        return "No tasks found."

    # 表头
    header = f"{'Status':<12} {'Model':<35} {'Task ID':<12} {'Created':<20}"
    separator = "-" * len(header)
    lines = [header, separator]

    # 任务行
    for task in tasks:
        status = task.get("status", "")
        model = task.get("model", "")
        task_id = task.get("id", "")
        created = task.get("created", "")[:19]  # 截断到秒

        # 截断过长的 model 名称
        if len(model) > 32:
            model = model[:29] + "..."

        # 截断任务 ID
        if len(task_id) > 10:
            task_id = task_id[:8] + ".."

        lines.append(f"{status:<12} {model:<35} {task_id:<12} {created:<20}")

    # 分页信息
    lines.append("")
    page_num = page_info.get("page_num", 0)
    page_size = page_info.get("page_size", 0)
    total = page_info.get("total", 0)
    total_pages = (total + page_size - 1) // page_size if page_size > 0 else 0

    lines.append(f"Page {page_num}/{total_pages} | Total tasks: {total}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="List video generation tasks with filtering and pagination",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # List all tasks
  python list_tasks.py

  # Filter by status
  python list_tasks.py --status succeeded

  # Filter by model
  python list_tasks.py --model doubao-seedance-1-5-pro-251215

  # Pagination
  python list_tasks.py --page-num 2 --page-size 20

  # Filter by specific task IDs
  python list_tasks.py --task-ids task1,task2,task3
        """
    )

    # 筛选参数
    parser.add_argument(
        "--status",
        type=str,
        choices=["queued", "running", "succeeded", "failed", "cancelled", "expired"],
        help="Filter by task status"
    )
    parser.add_argument(
        "--model",
        type=str,
        help="Filter by model ID"
    )
    parser.add_argument(
        "--task-ids",
        type=str,
        help="Comma-separated list of specific task IDs"
    )

    # 分页参数
    parser.add_argument(
        "--page-num",
        type=int,
        default=1,
        help="Page number (default: 1)"
    )
    parser.add_argument(
        "--page-size",
        type=int,
        default=10,
        help="Results per page, max 500 (default: 10)"
    )

    # 认证
    parser.add_argument(
        "--api-key",
        type=str,
        help="Override API Key"
    )

    # 输出格式
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output raw JSON"
    )

    args = parser.parse_args()

    # 验证参数
    if args.page_num < 1:
        parser.error("--page-num must be >= 1")

    if args.page_size < 1 or args.page_size > 500:
        parser.error("--page-size must be between 1 and 500")

    # 解析任务 ID 列表
    task_ids = None
    if args.task_ids:
        task_ids = [tid.strip() for tid in args.task_ids.split(",")]

    try:
        client = SeedanceClient(api_key=args.api_key)
        data = client.list_tasks(
            page_num=args.page_num,
            page_size=args.page_size,
            status=args.status,
            model=args.model,
            task_ids=task_ids
        )

        if args.json:
            import json
            print(json.dumps(data, indent=2, ensure_ascii=False))
        else:
            print(format_task_list(data))

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

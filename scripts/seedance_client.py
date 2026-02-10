#!/usr/bin/env python3
"""
Seedance API Client

核心客户端类，用于与 Volcengine Seedance API 交互。
提供视频生成任务的创建、查询、列表和取消功能。
"""

import os
import time
import json
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from enum import Enum

try:
    import requests
    from dotenv import load_dotenv
except ImportError as e:
    raise ImportError(
        f"Missing required dependency: {e.name}. "
        "Install with: pip install -r requirements.txt"
    )


class TaskStatus(Enum):
    """任务状态枚举"""
    QUEUED = "queued"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    EXPIRED = "expired"
    CANCELLED = "cancelled"


class SeedanceError(Exception):
    """Seedance API 基础异常"""
    pass


class AuthenticationError(SeedanceError):
    """认证错误"""
    pass


class MissingAPIKeyError(AuthenticationError):
    """缺少 API Key 错误"""
    pass


class APIError(SeedanceError):
    """API 请求错误"""
    def __init__(self, message: str, status_code: Optional[int] = None, response: Optional[Dict] = None):
        super().__init__(message)
        self.status_code = status_code
        self.response = response


class InvalidRequestError(APIError):
    """无效请求错误"""
    pass


class RateLimitError(APIError):
    """限流错误"""
    pass


class TaskNotFoundError(SeedanceError):
    """任务未找到错误"""
    pass


class NetworkError(SeedanceError):
    """网络错误"""
    pass


class TimeoutError(SeedanceError):
    """超时错误"""
    pass


@dataclass
class TaskInfo:
    """任务信息"""
    id: str
    status: TaskStatus
    model: str
    created_at: str
    video_url: Optional[str] = None
    last_frame_url: Optional[str] = None
    resolution: Optional[str] = None
    ratio: Optional[str] = None
    duration: Optional[int] = None
    error_message: Optional[str] = None
    usage: Optional[Dict[str, Any]] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TaskInfo":
        """从字典创建 TaskInfo"""
        try:
            status = TaskStatus(data.get("status", "queued"))
        except ValueError:
            status = TaskStatus.QUEUED

        content = data.get("content", {})
        usage = data.get("usage", {})

        return cls(
            id=data.get("id", ""),
            status=status,
            model=data.get("model", ""),
            created_at=data.get("created_at", ""),
            video_url=content.get("video_url"),
            last_frame_url=content.get("last_frame_url"),
            resolution=data.get("resolution"),
            ratio=data.get("ratio"),
            duration=data.get("duration"),
            error_message=data.get("error_message"),
            usage=usage
        )


class SeedanceClient:
    """Seedance API 客户端"""

    DEFAULT_BASE_URL = "https://ark.cn-beijing.volces.com/api/v3"
    DEFAULT_TIMEOUT = 60
    MAX_RETRIES = 3
    RETRY_DELAYS = [1, 2, 4]  # 秒

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: int = DEFAULT_TIMEOUT
    ):
        """
        初始化客户端

        Args:
            api_key: API Key，如果为 None 则从环境变量或 .env 文件读取
            base_url: API 基础 URL，默认为官方 URL
            timeout: 请求超时时间（秒）
        """
        self.api_key = api_key or self._get_api_key()
        self.base_url = (base_url or self.DEFAULT_BASE_URL).rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        })

    def _get_api_key(self) -> str:
        """
        获取 API Key

        优先级：
        1. VOLCENGINE_API_KEY 环境变量
        2. 当前目录 .env 文件中的 VOLCENGINE_API_KEY
        3. 交互式提示
        """
        # 尝试环境变量
        api_key = os.environ.get("VOLCENGINE_API_KEY")
        if api_key:
            return api_key

        # 尝试 .env 文件
        load_dotenv()
        api_key = os.environ.get("VOLCENGINE_API_KEY")
        if api_key:
            return api_key

        raise MissingAPIKeyError(
            "API Key not found. Set VOLCENGINE_API_KEY environment variable, "
            "add it to .env file, or pass --api-key parameter."
        )

    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict] = None,
        params: Optional[Dict] = None,
        retry_count: int = 0
    ) -> Dict[str, Any]:
        """
        发送 HTTP 请求（带重试）

        Args:
            method: HTTP 方法
            endpoint: API 端点
            data: 请求体数据
            params: URL 查询参数
            retry_count: 当前重试次数

        Returns:
            响应 JSON 数据

        Raises:
            SeedanceError: 请求失败
        """
        url = f"{self.base_url}{endpoint}"

        try:
            response = self.session.request(
                method=method,
                url=url,
                json=data,
                params=params,
                timeout=self.timeout
            )

            # 处理响应
            return self._handle_response(response)

        except requests.exceptions.Timeout:
            if retry_count < self.MAX_RETRIES:
                delay = self.RETRY_DELAYS[min(retry_count, len(self.RETRY_DELAYS) - 1)]
                time.sleep(delay)
                return self._make_request(method, endpoint, data, params, retry_count + 1)
            raise TimeoutError(f"Request timeout after {self.timeout}s")

        except requests.exceptions.ConnectionError as e:
            raise NetworkError(f"Connection error: {e}")

        except requests.exceptions.RequestException as e:
            raise NetworkError(f"Request error: {e}")

    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """
        处理 API 响应

        Args:
            response: requests Response 对象

        Returns:
            响应 JSON 数据

        Raises:
            APIError: API 返回错误
        """
        try:
            data = response.json()
        except json.JSONDecodeError:
            data = {}

        # 成功响应
        if response.status_code == 200:
            return data

        # 认证错误
        if response.status_code == 401:
            raise AuthenticationError("Invalid API Key or authentication failed")

        # 任务未找到
        if response.status_code == 404:
            raise TaskNotFoundError("Task not found")

        # 限流错误
        if response.status_code == 429:
            raise RateLimitError("Rate limit exceeded. Please wait and retry.")

        # 其他 4xx 错误
        if 400 <= response.status_code < 500:
            error_msg = data.get("error", {}).get("message", "Invalid request")
            raise InvalidRequestError(
                error_msg,
                status_code=response.status_code,
                response=data
            )

        # 5xx 错误 - 可以重试
        if response.status_code >= 500:
            raise APIError(
                f"Server error: {response.status_code}",
                status_code=response.status_code,
                response=data
            )

        raise APIError(
            f"Unexpected status code: {response.status_code}",
            status_code=response.status_code,
            response=data
        )

    def create_task(self, payload: Dict[str, Any]) -> TaskInfo:
        """
        创建视频生成任务

        Args:
            payload: 任务创建参数

        Returns:
            TaskInfo 对象

        Raises:
            APIError: 创建失败
        """
        endpoint = "/contents/generations/tasks"
        data = self._make_request("POST", endpoint, data=payload)

        # 返回任务状态，因为 create 接口可能返回 task_id 或完整任务信息
        if "id" in data:
            return TaskInfo.from_dict(data)
        elif "task_id" in data:
            # 返回 task_id 的情况，需要查询获取完整信息
            task_id = data["task_id"]
            return self.get_task(task_id)
        else:
            raise APIError("Unexpected response format: missing task id")

    def get_task(self, task_id: str) -> TaskInfo:
        """
        查询单个任务状态

        Args:
            task_id: 任务 ID

        Returns:
            TaskInfo 对象

        Raises:
            TaskNotFoundError: 任务不存在
        """
        endpoint = f"/contents/generations/tasks/{task_id}"
        data = self._make_request("GET", endpoint)
        return TaskInfo.from_dict(data)

    def list_tasks(
        self,
        page_num: int = 1,
        page_size: int = 10,
        status: Optional[str] = None,
        model: Optional[str] = None,
        task_ids: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        列出任务（支持筛选和分页）

        Args:
            page_num: 页码（从 1 开始）
            page_size: 每页数量（最大 500）
            status: 按状态筛选
            model: 按模型筛选
            task_ids: 特定任务 ID 列表

        Returns:
            响应数据，包含 tasks 列表和分页信息
        """
        endpoint = "/contents/generations/tasks"

        params = {
            "page_num": page_num,
            "page_size": min(page_size, 500)
        }

        # 添加筛选参数
        filters = {}
        if status:
            filters["status"] = status
        if model:
            filters["model"] = model
        if task_ids:
            filters["task_ids"] = ",".join(task_ids)

        if filters:
            params["filter"] = filters

        return self._make_request("GET", endpoint, params=params)

    def cancel_task(self, task_id: str) -> Dict[str, Any]:
        """
        取消或删除任务

        取消队列中的任务，或删除已完成/失败的任务记录

        Args:
            task_id: 任务 ID

        Returns:
            响应数据
        """
        endpoint = f"/contents/generations/tasks/{task_id}"
        return self._make_request("DELETE", endpoint)

    def wait_for_completion(
        self,
        task_id: str,
        poll_interval: int = 5,
        timeout: int = 600,
        callback: Optional[callable] = None
    ) -> TaskInfo:
        """
        等待任务完成

        Args:
            task_id: 任务 ID
            poll_interval: 轮询间隔（秒）
            timeout: 超时时间（秒）
            callback: 回调函数，参数为 TaskInfo

        Returns:
            完成的 TaskInfo 对象

        Raises:
            TimeoutError: 超时
        """
        start_time = time.time()

        while True:
            task = self.get_task(task_id)

            # 调用回调
            if callback:
                callback(task)

            # 检查是否完成
            if task.status in (TaskStatus.SUCCEEDED, TaskStatus.FAILED,
                               TaskStatus.EXPIRED, TaskStatus.CANCELLED):
                return task

            # 检查超时
            elapsed = time.time() - start_time
            if elapsed >= timeout:
                raise TimeoutError(f"Task did not complete within {timeout}s")

            # 等待
            time.sleep(poll_interval)

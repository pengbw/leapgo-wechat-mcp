"""
access_token 管理：自动获取 + 缓存 + 自动刷新
"""
import time
import httpx
from .config import APP_ID, APP_SECRET, WECHAT_API_BASE

_token_cache = {"token": None, "expires_at": 0}


def get_access_token() -> str:
    """
    获取 access_token，优先使用缓存，token 过期前自动刷新
    """
    global _token_cache

    # 提前 5 分钟刷新，避免临界过期
    if _token_cache["token"] and time.time() < _token_cache["expires_at"] - 300:
        return _token_cache["token"]

    url = f"{WECHAT_API_BASE}/cgi-bin/token"
    params = {"grant_type": "client_credential", "appid": APP_ID, "secret": APP_SECRET}

    with httpx.Client(timeout=30) as client:
        resp = client.get(url, params=params)
        resp.raise_for_status()
        data = resp.json()

    if "access_token" not in data:
        raise RuntimeError(f"获取 access_token 失败: {data}")

    _token_cache["token"] = data["access_token"]
    _token_cache["expires_at"] = time.time() + data["expires_in"]

    return _token_cache["token"]

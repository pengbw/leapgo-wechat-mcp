"""
素材管理工具：上传图片、视频、音频
"""
import json
import httpx
from pathlib import Path
from ..auth import get_access_token


def upload_image(file_path: str) -> dict:
    """
    上传图片永久素材

    Args:
        file_path: 本地图片路径（支持 jpg/png/gif，大小不超过 2MB）
    """
    token = get_access_token()
    with open(file_path, 'rb') as f:
        resp = httpx.post(
            "https://api.weixin.qq.com/cgi-bin/material/add_material",
            params={"access_token": token, "type": "image"},
            files={"media": (Path(file_path).name, f, "image/jpeg")},
            timeout=30
        )
    return resp.json()


def upload_video(file_path: str, title: str = "视频标题", introduction: str = "") -> dict:
    """
    上传视频永久素材

    Args:
        file_path: 本地视频路径（mp4，大小不超过 10MB）
        title: 视频标题
        introduction: 视频简介
    """
    token = get_access_token()
    with open(file_path, 'rb') as f:
        resp = httpx.post(
            "https://api.weixin.qq.com/cgi-bin/material/add_material",
            params={"access_token": token, "type": "video"},
            files={"media": (Path(file_path).name, f, "video/mp4")},
            data={
                "description": json.dumps({
                    "title": title,
                    "introduction": introduction
                }, ensure_ascii=False)
            },
            timeout=60
        )
    return resp.json()


def upload_voice(file_path: str) -> dict:
    """
    上传音频永久素材（语音）

    Args:
        file_path: 本地音频路径（mp3/wma/wav/amr，大小不超过 10MB）
    """
    token = get_access_token()
    ext = Path(file_path).suffix.lower().lstrip('.')
    mime = f"audio/{ext}" if ext in ("mp3", "wav", "amr") else "audio/mpeg"
    with open(file_path, 'rb') as f:
        resp = httpx.post(
            "https://api.weixin.qq.com/cgi-bin/material/add_material",
            params={"access_token": token, "type": "voice"},
            files={"media": (Path(file_path).name, f, mime)},
            timeout=60
        )
    return resp.json()


def list_materials(material_type: str = "image", offset: int = 0, count: int = 20) -> dict:
    """
    列出永久素材

    Args:
        material_type: image / video / voice / news
        offset: 偏移量
        count: 每页数量
    """
    token = get_access_token()
    resp = httpx.post(
        f"https://api.weixin.qq.com/cgi-bin/material/batchget_material?access_token={token}",
        json={"type": material_type, "offset": offset, "count": count},
        timeout=30
    )
    return resp.json()

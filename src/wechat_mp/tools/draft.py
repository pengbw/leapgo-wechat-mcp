"""
草稿箱工具：创建、列出(分页)、获取(详情)、更新、删除草稿
"""
import httpx
from ..auth import get_access_token

DEFAULT_THUMB_MEDIA_ID = "RSxJjhu3qD2mcXqa9dM93diGSnoU3UGyfa7H3QMfEpR6o2AJh76soDtR-asum4OY"


def create_draft(title: str, author: str, content: str, digest: str = "",
                  thumb_media_id: str = DEFAULT_THUMB_MEDIA_ID) -> dict:
    """
    新增草稿
    """
    token = get_access_token()
    url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={token}"
    articles = [{
        "title": title,
        "author": author,
        "digest": digest or content[:54],
        "content": content,
        "thumb_media_id": thumb_media_id,
        "need_open_comment": 1,
        "only_fans_can_comment": 0,
    }]
    with httpx.Client(timeout=30) as client:
        resp = client.post(url, json={"articles": articles})
        resp.raise_for_status()
        return resp.json()


def list_drafts(offset: int = 0, count: int = 20) -> dict:
    """
    批量获取草稿列表（分页）

    Returns:
        {
          "total_count": int,        # 总草稿数
          "item_count": int,         # 本页条数
          "item": [
            {
              "media_id": str,
              "update_time": int,    # 更新时间戳
              "create_time": int,    # 创建时间戳
              "content": {
                "news_item": [{
                  "title": str,
                  "author": str,
                  "digest": str,
                  "thumb_url": str,  # 封面图URL
                  "need_open_comment": int,
                  "only_fans_can_comment": int,
                }]
              }
            }
          ]
        }
    """
    token = get_access_token()
    url = f"https://api.weixin.qq.com/cgi-bin/draft/batchget?access_token={token}"
    payload = {"offset": offset, "count": count, "no_content": 0}
    with httpx.Client(timeout=30) as client:
        resp = client.post(url, json=payload)
        resp.raise_for_status()
        return resp.json()


def get_draft(media_id: str) -> dict:
    """
    获取草稿详情（含完整正文内容）
    """
    token = get_access_token()
    url = f"https://api.weixin.qq.com/cgi-bin/draft/get?access_token={token}"
    with httpx.Client(timeout=30) as client:
        resp = client.post(url, json={"media_id": media_id})
        resp.raise_for_status()
        result = resp.json()
        # 格式化输出，方便阅读
        if result.get("news_item"):
            item = result["news_item"][0]
            result["_info"] = {
                "media_id": media_id,
                "title": item.get("title"),
                "author": item.get("author"),
                "digest": item.get("digest"),
                "thumb_url": item.get("thumb_url"),
                "content_length": len(item.get("content", "")),
                "url": item.get("url"),  # 预览URL
            }
        return result


def update_draft(media_id: str, title: str = None, author: str = None,
                  content: str = None, digest: str = None,
                  thumb_media_id: str = None) -> dict:
    """
    更新草稿内容（支持部分更新，只传需要改的字段）

    Args:
        media_id: 草稿 media_id（必填）
        title: 新标题
        author: 新作者
        content: 新正文
        digest: 新摘要
        thumb_media_id: 新封面图 media_id
    """
    token = get_access_token()
    # 先拉取原内容
    original = get_draft(media_id)
    if original.get("news_item"):
        item = original["news_item"][0]
    else:
        item = {}

    article = {
        "media_id": media_id,
        "title": title if title is not None else item.get("title", ""),
        "author": author if author is not None else item.get("author", ""),
        "digest": digest if digest is not None else item.get("digest", ""),
        "content": content if content is not None else item.get("content", ""),
        "thumb_media_id": thumb_media_id if thumb_media_id is not None else item.get("thumb_media_id", DEFAULT_THUMB_MEDIA_ID),
        "need_open_comment": 1,
        "only_fans_can_comment": 0,
    }

    url = f"https://api.weixin.qq.com/cgi-bin/draft/update?access_token={token}"
    with httpx.Client(timeout=30) as client:
        resp = client.post(url, json={"articles": [article]})
        resp.raise_for_status()
        return resp.json()


def delete_draft(media_id: str) -> dict:
    """
    删除草稿
    """
    token = get_access_token()
    url = f"https://api.weixin.qq.com/cgi-bin/draft/delete?access_token={token}"
    with httpx.Client(timeout=30) as client:
        resp = client.post(url, json={"media_id": media_id})
        resp.raise_for_status()
        return resp.json()

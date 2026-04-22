"""
发布工具：提交发布、查看发布记录
"""
import httpx
from ..auth import get_access_token


def submit_publish(media_id: str) -> dict:
    """
    发布草稿箱中的文章

    Args:
        media_id: 草稿的 media_id
    """
    token = get_access_token()
    url = f"https://api.weixin.qq.com/cgi-bin/freepublish/submitpublish?access_token={token}"
    payload = {"media_id": media_id}
    with httpx.Client(timeout=30) as client:
        resp = client.post(url, json=payload)
        resp.raise_for_status()
        return resp.json()


def list_publish(offset: int = 0, count: int = 20) -> dict:
    """
    查看已发布文章的记录（分页）

    Returns:
        {
          "total_count": int,
          "item_count": int,
          "item": [
            {
              "msg_id": int,
              "article_id": str,
              "title": str,
              "author": str,
              "digest": str,
              "thumb_url": str,
              "url": str,
              "publish_status": int,
              "publish_time": int,
            }
          ]
        }
    """
    token = get_access_token()
    url = f"https://api.weixin.qq.com/cgi-bin/freepublish/batchget?access_token={token}"
    payload = {"offset": offset, "count": count}
    with httpx.Client(timeout=30) as client:
        resp = client.post(url, json=payload)
        resp.raise_for_status()
        return resp.json()


def delete_publish(article_id: str) -> dict:
    """
    删除已发布文章（公众号后台可删除）
    """
    token = get_access_token()
    url = f"https://api.weixin.qq.com/cgi-bin/draft/delete?access_token={token}"
    with httpx.Client(timeout=30) as client:
        resp = client.post(url, json={"media_id": article_id})
        resp.raise_for_status()
        return resp.json()

"""
数据统计工具
"""
import httpx
from ..auth import get_access_token


def stats_article(begin_date: str, end_date: str) -> dict:
    """
    获取图文群发数据（阅读量、分享、收藏等）

    Args:
        begin_date: 开始日期，格式 YYYYMMDD
        end_date: 结束日期，格式 YYYYMMDD
    """
    token = get_access_token()
    url = f"https://api.weixin.qq.com/cgi-bin/datacube/getarticlesummary?access_token={token}"
    payload = {"begin_date": begin_date, "end_date": end_date}
    with httpx.Client(timeout=30) as client:
        resp = client.post(url, json=payload)
        resp.raise_for_status()
        return resp.json()


def stats_user(begin_date: str, end_date: str) -> dict:
    """
    获取用户增减数据（新增/取消关注用户数）

    Args:
        begin_date: 开始日期，格式 YYYYMMDD
        end_date: 结束日期，格式 YYYYMMDD
    """
    token = get_access_token()
    url = f"https://api.weixin.qq.com/cgi-bin/datacube/getusersummary?access_token={token}"
    payload = {"begin_date": begin_date, "end_date": end_date}
    with httpx.Client(timeout=30) as client:
        resp = client.post(url, json=payload)
        resp.raise_for_status()
        return resp.json()


def stats_summary(begin_date: str, end_date: str) -> dict:
    """
    获取数据概览（图文阅读、用户增长、消息统计）

    Args:
        begin_date: 开始日期，格式 YYYYMMDD
        end_date: 结束日期，格式 YYYYMMDD
    """
    token = get_access_token()
    url = f"https://api.weixin.qq.com/cgi-bin/datacube/getupstreammsgdist?access_token={token}"
    payload = {"begin_date": begin_date, "end_date": end_date}
    with httpx.Client(timeout=30) as client:
        resp = client.post(url, json=payload)
        resp.raise_for_status()
        return resp.json()

"""
账号工具：查看公众号基本信息（含头像）
"""
import httpx
from ..auth import get_access_token


def account_info() -> dict:
    """
    获取公众号自动回复配置（微信API暂无直接获取公众号头像/昵称的接口）

    注意：微信公众平台 API 不提供直接获取公众号自身头像、昵称、原始ID等基本资料。
    如需查看，建议：
    1. 登录微信公众平台后台 https://mp.weixin.qq.com 直接查看
    2. 或者通过用户信息接口间接获取（粉丝头像等信息）
    """
    token = get_access_token()
    url = f"https://api.weixin.qq.com/cgi-bin/get_current_autoreply_info?access_token={token}"
    with httpx.Client(timeout=30) as client:
        resp = client.get(url)
        resp.raise_for_status()
        return resp.json()


def get_followers(next_openid: str = None) -> dict:
    """
    获取关注者列表（含基本信息）

    Args:
        next_openid: 下一个openid，不传则从第一个开始
    """
    token = get_access_token()
    url = f"https://api.weixin.qq.com/cgi-bin/user/get?access_token={token}"
    params = {}
    if next_openid:
        params["next_openid"] = next_openid
    with httpx.Client(timeout=30) as client:
        resp = client.get(url, params=params)
        resp.raise_for_status()
        return resp.json()


def get_user_info(openid: str) -> dict:
    """
    获取单个用户信息（含头像、性别、地区、关注时间）

    Args:
        openid: 用户openid
    """
    token = get_access_token()
    url = f"https://api.weixin.qq.com/cgi-bin/user/info?access_token={token}&openid={openid}&lang=zh_CN"
    with httpx.Client(timeout=30) as client:
        resp = client.get(url)
        resp.raise_for_status()
        return resp.json()


def batch_get_user_info(openids: list[str]) -> dict:
    """
    批量获取用户信息（最多100个openid）

    Args:
        openids: openid列表
    """
    token = get_access_token()
    url = f"https://api.weixin.qq.com/cgi-bin/user/info/batchget?access_token={token}"
    user_list = [{"openid": oid, "lang": "zh_CN"} for oid in openids[:100]]
    with httpx.Client(timeout=30) as client:
        resp = client.post(url, json={"user_list": user_list})
        resp.raise_for_status()
        return resp.json()

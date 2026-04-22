import os
from dotenv import load_dotenv

load_dotenv()

# 微信公众号账号
APP_ID = os.getenv("WECHAT_APP_ID", "wxdd6181c2c086c7bf")
APP_SECRET = os.getenv("WECHAT_APP_SECRET", "cc2bb4f90c3a0374b60e285708f58a12")

# 微信 API
WECHAT_API_BASE = "https://api.weixin.qq.com"

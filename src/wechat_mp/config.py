import os
from dotenv import load_dotenv

load_dotenv()

# 微信公众号账号
APP_ID = os.getenv("WECHAT_APP_ID", "wxdd6181c2c086c7bf")
APP_SECRET = os.getenv("WECHAT_APP_SECRET", "cc2bb****58a12")

# 微信 API
WECHAT_API_BASE = "https://api.weixin.qq.com"

"""
Markdown 工具：Markdown 转微信友好 HTML（行内样式版）
"""
import mistune
from bs4 import BeautifulSoup


# 微信文章样式（行内 CSS，非 <style> 标签）
WECHAT_STYLES = {
    "section": (
        'font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", '
        '"Hiragino Sans GB", "Microsoft YaHei", sans-serif; '
        "font-size: 16px; line-height: 1.8; color: #333;"
    ),
    "h2": (
        "font-size: 20px; font-weight: bold; margin: 24px 0 12px; "
        'color: #1a1a1a; border-left: 4px solid #4fc3f7; padding-left: 12px;'
    ),
    "h3": "font-size: 17px; font-weight: bold; margin: 16px 0 8px; color: #333;",
    "p": "margin: 12px 0; line-height: 1.8;",
    "ul": "padding-left: 24px; margin: 12px 0;",
    "ol": "padding-left: 24px; margin: 12px 0;",
    "li": "margin: 6px 0;",
    "blockquote": (
        "background: #f8f9fa; border-left: 4px solid #4fc3f7; "
        "margin: 16px 0; padding: 12px 16px; border-radius: 0 6px 6px 0;"
    ),
    "code": (
        "background: #f4f4f4; padding: 2px 6px; border-radius: 4px; "
        'font-family: "SF Mono", Consolas, monospace; font-size: 14px;'
    ),
    "pre": (
        "background: #1e1e1e; color: #d4d4d4; padding: 16px; border-radius: 8px; "
        "overflow-x: auto; margin: 16px 0;"
    ),
    "img": "max-width: 100%; border-radius: 6px; display: block; margin: 16px auto;",
    "hr": "border: none; border-top: 1px dashed #ddd; margin: 24px 0;",
    "table": "border-collapse: collapse; width: 100%; margin: 16px 0;",
    "th": (
        "background: #f8f9fa; font-weight: bold; padding: 8px 12px; "
        "border: 1px solid #ddd; text-align: left;"
    ),
    "td": "padding: 8px 12px; border: 1px solid #ddd; text-align: left;",
}

# 每个 tr 的斑马条纹背景色
ZEBRA_BG = ["background: #ffffff;", "background: #fafafa;"]

# mistune 插件列表
MARKDOWN_PLUGINS = ["table"]


def md_to_html(markdown: str) -> str:
    """
    将 Markdown 转换为微信友好的带样式 HTML（行内样式）。

    支持：
    - h2 / h3 标题（蓝左边框亮蓝）
    - 段落 / 列表 / 引用块
    - 代码块（暗色主题）
    - 表格（斑马纹）
    - 图片 / 分割线

    Args:
        markdown: Markdown 格式的文本

    Returns:
        纯净 HTML 字符串（无 <html>/<body>/<style> 标签），可直接用于微信草稿 API
    """
    md = mistune.create_markdown(plugins=MARKDOWN_PLUGINS)
    raw_html = md(markdown)

    # 用 lxml 解析器保证 HTML 结构完整
    soup = BeautifulSoup(f"<div>{raw_html}</div>", "lxml")
    div = soup.div

    # 创建带基础样式的 section 包裹
    section = soup.new_tag("section", style=WECHAT_STYLES["section"])
    for child in list(div.children):
        section.append(child.extract())

    # 清除临时 div，保留 section
    soup.append(section)

    # 表格整体样式
    for tbl in soup.find_all("table"):
        tbl["style"] = WECHAT_STYLES["table"]

    # 斑马纹（每行交替背景）
    for i, tr in enumerate(soup.find_all("tr")):
        tr["style"] = ZEBRA_BG[i % 2]
        # th/td 各自已有样式，不再覆盖

    # 各标签行内样式（pre 内的 code 单独处理，不加背景色）
    for tag, style in WECHAT_STYLES.items():
        if tag in ("section", "table", "tr", "code"):
            continue  # code 在 pre 内时不加背景色
        for el in soup.find_all(tag):
            el["style"] = style

    # pre 内的 code（代码内容）去掉背景色，保持透明融入暗色 pre 背景
    for code in soup.find_all("pre"):
        for c in code.find_all("code"):
            c["style"] = (
                "background: transparent; padding: 0; border-radius: 0; "
                'font-family: "SF Mono", Consolas, monospace; font-size: 14px;'
            )

    # 引用块内的 <p> 去掉（保留文字，去掉包裹）
    for bq in soup.find_all("blockquote"):
        for p in bq.find_all("p"):
            p.unwrap()

    # 去掉所有 <div> 临时标签（table 插件可能生成）
    for div in soup.find_all("div"):
        div.unwrap()

    # 只返回 section 内容，不带 <html><body>
    return str(soup.find("section"))


def apply_theme(html_content: str, theme: str = "default") -> str:
    """
    为已有 HTML 内容应用主题（暂保留兼容，主题逻辑未来扩展）。

    Args:
        html_content: 原始 HTML 内容
        theme: 主题名称（default / minimal / dark）
    """
    # 当前版本 md_to_html 已内置样式，apply_theme 暂不处理
    # 后续可扩展：minimal 去掉蓝边框、dark 反色主题
    return html_content


def preview_html(html_content: str) -> dict:
    """
    生成可预览的 HTML 文件路径。

    Args:
        html_content: HTML 内容

    Returns:
        {"path": "/tmp/wx_preview_xxxxx.html"}
    """
    import os
    import tempfile

    fd, preview_path = tempfile.mkstemp(suffix=".html", prefix="wx_preview_")
    full_html = (
        "<!DOCTYPE html>"
        '<html lang="zh-CN">'
        "<head><meta charset=\"utf-8\">"
        "<title>微信预览</title></head>"
        f"<body style='max-width:800px;margin:0 auto;padding:20px;'>{html_content}</body>"
        "</html>"
    )
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(full_html)
    return {"path": preview_path}

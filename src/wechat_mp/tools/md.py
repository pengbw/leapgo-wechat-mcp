"""
Markdown 工具：Markdown 转 HTML、应用主题、预览
"""
import re


DEFAULT_THEME = """
<style>
.wx-article {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
    font-size: 16px;
    line-height: 1.8;
    color: #333;
    max-width: 100%;
    padding: 0;
}
.wx-article h1 { font-size: 24px; font-weight: bold; margin: 24px 0 16px; color: #1a1a1a; }
.wx-article h2 { font-size: 20px; font-weight: bold; margin: 20px 0 12px; color: #1a1a1a; border-left: 4px solid #4C4C4C; padding-left: 12px; }
.wx-article h3 { font-size: 17px; font-weight: bold; margin: 16px 0 8px; color: #333; }
.wx-article p { margin: 12px 0; }
.wx-article ul, .wx-article ol { padding-left: 24px; margin: 12px 0; }
.wx-article li { margin: 6px 0; }
.wx-article blockquote {
    background: #f8f9fa;
    border-left: 4px solid #ddd;
    margin: 16px 0;
    padding: 12px 16px;
    border-radius: 0 6px 6px 0;
}
.wx-article code {
    background: #f4f4f4;
    padding: 2px 6px;
    border-radius: 4px;
    font-family: "SF Mono", Consolas, monospace;
    font-size: 14px;
}
.wx-article pre {
    background: #1e1e1e;
    color: #d4d4d4;
    padding: 16px;
    border-radius: 8px;
    overflow-x: auto;
    margin: 16px 0;
}
.wx-article img { max-width: 100%; border-radius: 6px; display: block; margin: 16px auto; }
.wx-article hr { border: none; border-top: 1px dashed #ddd; margin: 24px 0; }
.wx-article table { border-collapse: collapse; width: 100%; margin: 16px 0; }
.wx-article table th, .wx-article table td { border: 1px solid #ddd; padding: 8px 12px; text-align: left; }
.wx-article table th { background: #f8f9fa; font-weight: bold; }
.wx-article a { color: #4C4C4C; text-decoration: none; }
.wx-article .highlight-green { color: #2ecc71; font-weight: bold; }
.wx-article .highlight-orange { color: #f39c12; font-weight: bold; }
.wx-article .tag-block { background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0; line-height: 2; }
</style>
"""


def md_to_html(markdown: str) -> str:
    """
    将 Markdown 转换为微信友好的 HTML

    Args:
        markdown: Markdown 格式的文本
    """
    import mistune
    html = mistune.html(markdown)
    return html


def apply_theme(html_content: str, theme: str = "default") -> str:
    """
    为 HTML 应用指定主题样式

    Args:
        html_content: 原始 HTML 内容
        theme: 主题名称（default / minimal / dark）
    """
    if theme == "minimal":
        css = """
        <style>
        .wx-article { font-family: -apple-system, sans-serif; font-size: 15px; line-height: 1.7; color: #444; }
        .wx-article h2 { border-left: none; padding-left: 0; color: #222; }
        .wx-article blockquote { background: #fff; border-left: 2px solid #ccc; }
        </style>
        """
    elif theme == "dark":
        css = """
        <style>
        .wx-article { background: #1a1a1a; color: #ccc; font-family: -apple-system, sans-serif; font-size: 15px; line-height: 1.7; padding: 20px; }
        .wx-article h1, .wx-article h2, .wx-article h3 { color: #fff; }
        .wx-article blockquote { background: #2a2a2a; border-left-color: #555; }
        .wx-article code { background: #2a2a2a; }
        </style>
        """
    else:
        css = DEFAULT_THEME

    # 如果内容已有 class，直接追加样式
    if 'class="wx-article"' not in html_content:
        html_content = f'<div class="wx-article">{html_content}</div>'

    return css + html_content


def preview_html(html_content: str) -> dict:
    """
    生成可预览的 HTML 文件路径（写入临时文件，跨平台兼容）

    Args:
        html_content: HTML 内容

    Returns:
        {"path": "C:\\Users\\xxx\\AppData\\Local\\Temp\\wx_preview.html"}  (Windows)
        {"path": "/tmp/wx_preview.html"}                                   (Linux/macOS)
    """
    import tempfile
    import os

    fd, preview_path = tempfile.mkstemp(suffix=".html", prefix="wx_preview_")
    # 写入内容
    full_html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>微信预览</title></head>
<body style="max-width:800px;margin:0 auto;padding:20px;">{html_content}</body></html>"""
    with os.fdopen(fd, 'w', encoding='utf-8') as f:
        f.write(full_html)
    return {"path": preview_path}

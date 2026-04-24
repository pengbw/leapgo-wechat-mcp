"""
leapgo-wechat-mcp: 微信公众号 MCP Server
全工具注册入口 v0.2
"""
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
from typing import Any

from .tools.draft import create_draft, list_drafts, get_draft, update_draft, delete_draft
from .tools.publish import submit_publish, list_publish
from .tools.stats import stats_article, stats_user, stats_summary
from .tools.account import account_info, get_followers, get_user_info, batch_get_user_info
from .tools.material import upload_image, upload_video, upload_voice, list_materials
from .tools.md import md_to_html, apply_theme, preview_html

APP = Server("wechat-mp-plugin")


@APP.list_tools()
async def list_tools() -> list[Tool]:
    return [
        # ========== 草稿箱 ==========
        Tool(
            name="draft_create",
            description="在微信公众号草稿箱创建一篇新文章",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "文章标题"},
                    "author": {"type": "string", "description": "作者名称"},
                    "content": {"type": "string", "description": "正文内容（支持HTML）"},
                    "digest": {"type": "string", "description": "摘要（可选）"},
                    "thumb_media_id": {"type": "string", "description": "封面图 media_id（可选）"},
                },
                "required": ["title", "author", "content"],
            },
        ),
        Tool(
            name="draft_list",
            description="获取微信公众号草稿箱列表（分页）",
            inputSchema={
                "type": "object",
                "properties": {
                    "offset": {"type": "integer", "description": "偏移量，默认0", "default": 0},
                    "count": {"type": "integer", "description": "每页数量，默认20，最大50", "default": 20},
                },
            },
        ),
        Tool(
            name="draft_get",
            description="获取草稿箱中某篇文章的详细内容（含正文、预览URL）",
            inputSchema={
                "type": "object",
                "properties": {
                    "media_id": {"type": "string", "description": "草稿的 media_id"},
                },
                "required": ["media_id"],
            },
        ),
        Tool(
            name="draft_update",
            description="更新草稿箱中某篇文章的内容（支持部分更新）",
            inputSchema={
                "type": "object",
                "properties": {
                    "media_id": {"type": "string", "description": "草稿的 media_id"},
                    "title": {"type": "string", "description": "新标题（可选）"},
                    "author": {"type": "string", "description": "新作者（可选）"},
                    "content": {"type": "string", "description": "新正文内容（可选）"},
                    "digest": {"type": "string", "description": "新摘要（可选）"},
                    "thumb_media_id": {"type": "string", "description": "新封面图 media_id（可选）"},
                },
                "required": ["media_id"],
            },
        ),
        Tool(
            name="draft_delete",
            description="删除草稿箱中的一篇文章",
            inputSchema={
                "type": "object",
                "properties": {
                    "media_id": {"type": "string", "description": "草稿的 media_id"},
                },
                "required": ["media_id"],
            },
        ),
        # ========== 发布 ==========
        Tool(
            name="publish_submit",
            description="将草稿箱中的文章正式发布",
            inputSchema={
                "type": "object",
                "properties": {
                    "media_id": {"type": "string", "description": "草稿的 media_id"},
                },
                "required": ["media_id"],
            },
        ),
        Tool(
            name="publish_list",
            description="查看已发布文章的记录列表（分页）",
            inputSchema={
                "type": "object",
                "properties": {
                    "offset": {"type": "integer", "description": "偏移量，默认0", "default": 0},
                    "count": {"type": "integer", "description": "每页数量，默认20", "default": 20},
                },
            },
        ),
        # ========== 数据统计 ==========
        Tool(
            name="stats_article",
            description="获取图文群发数据（阅读量、分享、收藏等）",
            inputSchema={
                "type": "object",
                "properties": {
                    "begin_date": {"type": "string", "description": "开始日期，格式 YYYYMMDD"},
                    "end_date": {"type": "string", "description": "结束日期，格式 YYYYMMDD"},
                },
                "required": ["begin_date", "end_date"],
            },
        ),
        Tool(
            name="stats_user",
            description="获取用户增减数据（新增/取消关注用户数）",
            inputSchema={
                "type": "object",
                "properties": {
                    "begin_date": {"type": "string", "description": "开始日期，格式 YYYYMMDD"},
                    "end_date": {"type": "string", "description": "结束日期，格式 YYYYMMDD"},
                },
                "required": ["begin_date", "end_date"],
            },
        ),
        Tool(
            name="stats_summary",
            description="获取数据概览（消息统计）",
            inputSchema={
                "type": "object",
                "properties": {
                    "begin_date": {"type": "string", "description": "开始日期，格式 YYYYMMDD"},
                    "end_date": {"type": "string", "description": "结束日期，格式 YYYYMMDD"},
                },
                "required": ["begin_date", "end_date"],
            },
        ),
        # ========== 账号 & 用户 ==========
        Tool(
            name="account_info",
            description="获取公众号基本信息",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="followers_list",
            description="获取关注者列表",
            inputSchema={
                "type": "object",
                "properties": {
                    "next_openid": {"type": "string", "description": "下一个openid（分页用，不传则从第一个开始）"},
                },
            },
        ),
        Tool(
            name="user_info",
            description="获取单个用户详细信息（含头像、性别、地区、关注时间、语言）",
            inputSchema={
                "type": "object",
                "properties": {
                    "openid": {"type": "string", "description": "用户openid"},
                },
                "required": ["openid"],
            },
        ),
        Tool(
            name="user_batch_info",
            description="批量获取用户信息（最多100个openid，含头像）",
            inputSchema={
                "type": "object",
                "properties": {
                    "openids": {"type": "array", "items": {"type": "string"}, "description": "openid列表，最多100个"},
                },
                "required": ["openids"],
            },
        ),
        # ========== 素材 ==========
        Tool(
            name="material_upload_image",
            description="上传图片永久素材（支持 jpg/png/gif，最大 2MB）",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {"type": "string", "description": "本地图片文件路径"},
                },
                "required": ["file_path"],
            },
        ),
        Tool(
            name="material_upload_video",
            description="上传视频永久素材（mp4，最大 10MB）",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {"type": "string", "description": "本地视频文件路径"},
                    "title": {"type": "string", "description": "视频标题"},
                    "introduction": {"type": "string", "description": "视频简介"},
                },
                "required": ["file_path", "title"],
            },
        ),
        Tool(
            name="material_upload_voice",
            description="上传音频永久素材（mp3/wav/amr，最大 10MB）",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {"type": "string", "description": "本地音频文件路径"},
                },
                "required": ["file_path"],
            },
        ),
        Tool(
            name="material_list",
            description="列出永久素材（分页）",
            inputSchema={
                "type": "object",
                "properties": {
                    "material_type": {"type": "string", "description": "类型：image / video / voice，默认 image"},
                    "offset": {"type": "integer", "description": "偏移量，默认0"},
                    "count": {"type": "integer", "description": "每页数量，默认20"},
                },
            },
        ),
        # ========== Markdown ==========
        Tool(
            name="md_to_html",
            description="将 Markdown 转换为微信友好的 HTML",
            inputSchema={
                "type": "object",
                "properties": {
                    "markdown": {"type": "string", "description": "Markdown 格式的文本内容"},
                },
                "required": ["markdown"],
            },
        ),
        Tool(
            name="apply_theme",
            description="为 HTML 应用主题样式（default / minimal / dark）",
            inputSchema={
                "type": "object",
                "properties": {
                    "html_content": {"type": "string", "description": "原始 HTML 内容"},
                    "theme": {"type": "string", "description": "主题名称：default / minimal / dark", "default": "default"},
                },
                "required": ["html_content", "theme"],
            },
        ),
        Tool(
            name="preview_html",
            description="生成可预览的 HTML 文件，返回本地文件路径",
            inputSchema={
                "type": "object",
                "properties": {
                    "html_content": {"type": "string", "description": "HTML 内容"},
                },
                "required": ["html_content"],
            },
        ),
    ]


@APP.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    handlers = {
        # 草稿箱
        "draft_create": lambda a: create_draft(**a),
        "draft_list": lambda a: list_drafts(**a),
        "draft_get": lambda a: get_draft(**a),
        "draft_update": lambda a: update_draft(**a),
        "draft_delete": lambda a: delete_draft(**a),
        # 发布
        "publish_submit": lambda a: submit_publish(**a),
        "publish_list": lambda a: list_publish(**a),
        # 统计
        "stats_article": lambda a: stats_article(**a),
        "stats_user": lambda a: stats_user(**a),
        "stats_summary": lambda a: stats_summary(**a),
        # 账号 & 用户
        "account_info": lambda _: account_info(),
        "followers_list": lambda a: get_followers(**a),
        "user_info": lambda a: get_user_info(**a),
        "user_batch_info": lambda a: batch_get_user_info(**a),
        # 素材
        "material_upload_image": lambda a: upload_image(**a),
        "material_upload_video": lambda a: upload_video(**a),
        "material_upload_voice": lambda a: upload_voice(**a),
        "material_list": lambda a: list_materials(**a),
        # Markdown
        "md_to_html": lambda a: md_to_html(**a),
        "apply_theme": lambda a: apply_theme(**a),
        "preview_html": lambda a: preview_html(**a),
    }

    if name not in handlers:
        raise ValueError(f"未知工具: {name}")

    result = handlers[name](arguments)
    return [TextContent(type="text", text=str(result))]


async def main_http(port=8081):
    """HTTP mode for Hermes Agent MCP connection"""
    from mcp.server.sse import sse_server
    import asyncio
    
    from starlette.applications import Starlette
    from starlette.routing import Route
    from starlette.responses import JSONResponse
    import uvicorn
    
    write_stream = None
    read_stream = None
    
    async def handle_sse(request):
        global write_stream, read_stream
        from starlette.requests import Request
        req = Request(request)
        
        async def handle_messages():
            pass
        
        return JSONResponse({"status": "ok"})
    
    app = Starlette(routes=[Route('/mcp', handle_sse, methods=["GET", "POST"])])
    config = uvicorn.Config(app, host="0.0.0.0", port=port, log_level="error")
    server = uvicorn.Server(config)
    await server.serve()


async def main():
    """stdio mode — MCP client connects via stdin/stdout"""
    options = APP.create_initialization_options()
    async with stdio_server() as (read_stream, write_stream):
        await APP.run(read_stream, write_stream, options, raise_exceptions=True)


if __name__ == "__main__":
    import asyncio, sys
    if "--http" in sys.argv:
        port = int(sys.argv[sys.argv.index("--http") + 1]) if "--http" in sys.argv else 8081
        asyncio.run(main_http(port))
    else:
        asyncio.run(main())

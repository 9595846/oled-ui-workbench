"""MCP stdio tools operate only on named local preview drafts."""
import base64,io,os,sys
from pathlib import Path
vendor=Path(__file__).resolve().parent/'vendor'
vendor_dll_directory=None
if sys.prefix==sys.base_prefix:
    for part in [vendor,vendor/'win32',vendor/'win32/lib',vendor/'Pythonwin']:
        sys.path.insert(0,str(part))
    if sys.platform=='win32' and (vendor/'pywin32_system32').exists():
        vendor_dll_directory=os.add_dll_directory(str(vendor/'pywin32_system32'))
from mcp.server.fastmcp import FastMCP
import core
mcp=FastMCP('STM32 OLED 草稿预览')

@mcp.tool()
def read_draft(name: str='default') -> dict:
    """读取预览草稿。name 仅允许英文字母、数字、下划线、短横线。"""
    return core.load(name)

@mcp.tool()
def read_pages() -> dict:
    """读取已核对的原始四页模型与来源摘要；源文件变化需用 inspect_preview 核对。"""
    return core.defaults()

@mcp.tool()
def update_draft(name: str, draft: dict, expected_revision: int) -> dict:
    """用预期修订号保存整份草稿；若他人已更新则拒绝覆盖。"""
    return core.save(name,draft,expected_revision)

@mcp.tool()
def inspect_preview(name: str='default') -> dict:
    """检查当前页缺字、越界和源文件变化，并返回原始 128x64 PNG 的 base64。"""
    d=core.load(name);im,issues=core.render(d);buf=io.BytesIO();im.save(buf,format='PNG')
    return {'page':d['page'],'revision':d['revision'],'issues':issues,'source_changed':core.source_changed(d),'png_base64':base64.b64encode(buf.getvalue()).decode()}

@mcp.tool()
def export_ui(name: str, expected_revision: int) -> dict:
    """导出已保存的通用界面为待审阅 C 文件；不修改工程、不编译、不烧录。"""
    import exporter
    d=core.load(name)
    if d['revision']!=expected_revision:raise ValueError('草稿修订号已变化，请重新读取')
    return exporter.export(d,name)

if __name__=='__main__':mcp.run(transport='stdio')

import asyncio,json,sys,uuid,re,subprocess,urllib.request
from pathlib import Path
import mcp_server
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import core,studio

def unpack(result):
    assert not result.isError, result
    return json.loads(next(c.text for c in result.content if c.type=='text'))

async def main():
    name='test_mcp_'+uuid.uuid4().hex[:12]
    server=StdioServerParameters(command=sys.executable,args=['-X','utf8',str(Path(__file__).with_name('mcp_server.py'))])
    http=subprocess.Popen([sys.executable,'-X','utf8',str(Path(__file__).with_name('server.py')),'--no-browser'],stdout=subprocess.PIPE,text=True,encoding='utf-8')
    url=http.stdout.readline().strip().split('：',1)[1]
    html=urllib.request.urlopen(url).read().decode('utf-8')
    token=re.search(r"window.OLED_TOKEN='([^']+)'",html).group(1)
    def web(path,body=None):
        request=urllib.request.Request(url.rstrip('/')+path,headers={'X-OLED-Token':token,'Content-Type':'application/json'},data=json.dumps(body).encode() if body else None)
        return json.load(urllib.request.urlopen(request))
    try:
        async with stdio_client(server) as (read,write):
            async with ClientSession(read,write) as session:
                await session.initialize()
                assert {t.name for t in (await session.list_tools()).tools}=={'read_draft','read_pages','update_draft','inspect_preview','export_ui'}
                draft=unpack(await session.call_tool('read_pages',{}))
                draft['ideas']='MCP 与网页共用的测试草稿'
                updated=unpack(await session.call_tool('update_draft',{'name':name,'draft':draft,'expected_revision':0}))
                assert updated['revision']==1
                assert web('/api/draft?name='+name)['ideas']==draft['ideas']
                # Real HTTP write while the MCP stdio session remains open.
                assert web('/api/save',{'name':name,'draft':updated,'expected_revision':1})['revision']==2
                conflict=await session.call_tool('update_draft',{'name':name,'draft':updated,'expected_revision':1})
                assert conflict.isError
                readback=unpack(await session.call_tool('read_draft',{'name':name}))
                assert readback['revision']==2
                preview=unpack(await session.call_tool('inspect_preview',{'name':name}))
                assert preview['png_base64'].startswith('iVBOR') and not preview['source_changed']
                v2=studio.new();core.save(name,v2,2)
                exported=unpack(await session.call_tool('export_ui',{'name':name,'expected_revision':3}))
                assert 'ui_assets.c' in exported['files']
                stale=await session.call_tool('export_ui',{'name':name,'expected_revision':2});assert stale.isError
                invalid=await session.call_tool('read_draft',{'name':'../outside'})
                assert invalid.isError
                print('PASS: MCP stdio 四项工具、读写、PNG、共享修订冲突、路径限制')
    finally:
        http.terminate();http.wait(timeout=10)
        core.draft_path(name).unlink(missing_ok=True)
        out=core.ROOT/'exports'/name
        if out.exists():
            for f in out.iterdir():f.unlink()
            out.rmdir()
asyncio.run(main())

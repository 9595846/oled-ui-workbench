import json,re,subprocess,sys,urllib.request,urllib.error
from pathlib import Path
root=Path(__file__).resolve().parent
proc=subprocess.Popen([sys.executable,'-X','utf8',str(root/'server.py'),'--no-browser'],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,encoding='utf-8')
try:
    url=proc.stdout.readline().strip().split('：',1)[1]
    html=urllib.request.urlopen(url).read().decode('utf-8')
    token=re.search(r"window.OLED_TOKEN='([^']+)'",html).group(1)
    def call(path,method='GET',body=None,token_value=token):
        headers={'X-OLED-Token':token_value,'Content-Type':'application/json'}
        req=urllib.request.Request(url.rstrip('/')+path,headers=headers,method=method,data=json.dumps(body).encode() if body else None)
        return json.load(urllib.request.urlopen(req))
    try:call('/api/draft',token_value='bad');raise AssertionError('unauthorized accepted')
    except urllib.error.HTTPError as e:assert e.code==403
    draft=call('/api/default');assert len(draft['pages'])==4
    result=call('/api/render','POST',{'draft':draft});assert result['png'].startswith('iVBOR')
    draft['pages'][0][0]['text']='🦊';draft['pages'][0][0]['x']=125
    result=call('/api/render','POST',{'draft':draft});assert {x['type'] for x in result['issues']}=={'missing','overflow'}
    print('PASS: local HTTP authorization, render, missing glyph and overflow')
finally:
    proc.terminate();proc.wait(timeout=10)

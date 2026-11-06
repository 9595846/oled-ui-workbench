import os,sys,tempfile,subprocess,copy,ctypes
from pathlib import Path
import core,studio,exporter

def main():
 d=studio.new();d['pages'][0]['elements'][0]['text']='数值{value}';e=studio.element('dialog');e.update(id='dlg',mode='number');d['pages'][0]['elements'].append(e);d['pages'][0]['bindings']['KEY1']={'type':'open','target':'dlg'}
 d['pages'].append({'name':'图','elements':[dict(studio.element('image'),bits='10'*4096)],'bindings':{'KEY2':{'type':'goto','page':0}}});d['pages'][0]['bindings']['KEY4']={'type':'goto','page':1}
 files,m=exporter.generate(d)
 with tempfile.TemporaryDirectory(dir=core.ROOT) as tmp:
  root=Path(tmp)
  for n,c in files.items():(root/n).write_text(c,encoding='utf-8')
  hardware=core.FIRMWARE/'Hardware'
  (root/'host.c').write_text('#include "display.h"\nconst unsigned char *frame(void){return display_framebuffer();}\n')
  cmd=['gcc','-shared','-DMAZE_HOST_VIEW','-std=c99','-Wall','-Wextra','-Werror','-I'+str(root),'-I'+str(hardware),str(root/'ui_assets.c'),str(root/'ui_pages.c'),str(root/'ui_actions.c'),str(root/'host.c'),str(hardware/'display.c'),'-o',str(root/'test.dll')]
  cmd=[a.replace(str(root)+os.sep,'').replace('-I'+str(root),'-I.').replace(str(hardware),os.path.relpath(hardware,root)) for a in cmd]
  subprocess.run(cmd,check=True,cwd=root)
  lib=ctypes.CDLL(str(root/'test.dll'));lib.frame.restype=ctypes.POINTER(ctypes.c_ubyte);lib.ui_init()
  for event in [None,0,5,5,1,0,5,0,3,1]:
   if event is not None:d=studio.run(d,['KEY1','KEY2','KEY3','KEY4','LEFT','RIGHT'][event]);lib.ui_event(event)
   lib.ui_draw();im,_=studio.render(d);raw=lib.frame()
   assert all(bool(im.getpixel((x,y)))==bool(raw[(y//8)*128+x]&(1<<(y%8))) for y in range(64) for x in range(128)),event
   assert lib.ui_get_variable(0)==d['variables']['value']
  # Release host DLL before removing the temporary directory on Windows.
  import _ctypes
  _ctypes.FreeLibrary(lib._handle);del lib
  arm=Path('E:/keil5/ARM/ARMCC/bin/armcc.exe')
  if arm.exists():
   for name in ['ui_assets','ui_pages','ui_actions']:
    r=subprocess.run([str(arm),'--cpu','Cortex-M3','--c99','-c','-I.','-I'+os.path.relpath(hardware,root),name+'.c','-o',name+'.o'],capture_output=True,text=True,cwd=root)
    print(name,r.returncode,r.stdout,r.stderr);assert r.returncode==0
 print('PASS: generated C host compile; 10 state/frame comparisons; ARMCC compile (not full firmware link)')
 if not (core.ROOT/'exports'/'project_export_example').exists():
  d=studio.new();d['pages'][0]['elements'][0]['text']='数值{value}';d['pages'][0]['elements'].append(e);d['pages'][0]['bindings']['KEY1']={'type':'open','target':'dlg'};print(exporter.export(d,'project_export_example')['directory'])
if __name__=='__main__':main()


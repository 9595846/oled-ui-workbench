import unittest,copy,io,base64,tempfile
from pathlib import Path
from PIL import Image
import studio,core
class StudioTests(unittest.TestCase):
 def fixture(self):
  d=studio.new();e=studio.element('dialog');e.update(id='dialog',mode='number');d['pages'][0]['elements'].append(e);d['pages'][0]['bindings']['KEY1']={'type':'open','target':'dialog'};return d
 def test_number_confirm_cancel(self):
  d=self.fixture();opened=studio.run(d,'KEY1');changed=studio.run(opened,'RIGHT');self.assertEqual(d['variables']['value'],0);self.assertEqual(changed['input_value'],1)
  self.assertEqual(studio.run(changed,'KEY2')['variables']['value'],0);self.assertEqual(studio.run(changed,'KEY1')['variables']['value'],1)
 def test_jump_and_variables(self):
  d=self.fixture();d['pages'].append({'name':'第二页','elements':[],'bindings':{}});d['pages'][0]['elements'][1]['confirm']={'type':'goto','page':1};result=studio.run(studio.run(d,'KEY1'),'KEY1');self.assertEqual(result['page'],1);self.assertIsNone(result['active_dialog'])
  d['pages'][0]['bindings']['KEY2']={'type':'add','variable':'value','value':7};self.assertEqual(studio.run(d,'KEY2')['variables']['value'],7)
 def test_image(self):
  im=Image.new('RGB',(128,64),'black');b=io.BytesIO();im.save(b,format='PNG');e=studio.convert_image({'data':base64.b64encode(b.getvalue()).decode()});self.assertEqual(e['bits'],'1'*8192)
  d=studio.new();d['pages'][0]['elements']=[e];result,issues=studio.render(d);self.assertEqual(result.getpixel((127,63)),1);self.assertEqual(issues,[])
 def test_saved_v2_conflict(self):
  old=core.DRAFTS
  with tempfile.TemporaryDirectory() as tmp:
   core.DRAFTS=Path(tmp)
   try:
    d=self.fixture();core.save('project_test',d,0);self.assertEqual(core.load('project_test')['version'],2)
    with self.assertRaises(RuntimeError):core.save('project_test',d,0)
   finally:core.DRAFTS=old
 def test_missing_and_bad_references(self):
  d=studio.new();d['pages'][0]['elements'][0].update(text='🦊',x=125);_,issues=studio.render(d);self.assertEqual({i['type'] for i in issues},{'missing','overflow'})
  d['pages'][0]['bindings']['KEY1']={'type':'open','target':'nope'}
  with self.assertRaises(ValueError):studio.validate(d)
 def test_dialog_opaque(self):
  d=self.fixture();d=studio.run(d,'KEY1');a,_=studio.render(d);self.assertEqual(a.size,(128,64));self.assertEqual(a.getpixel((8,8)),1)
if __name__=='__main__':unittest.main(verbosity=2)

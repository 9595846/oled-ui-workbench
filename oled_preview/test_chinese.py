import unittest,sys
import studio,core,chinese_font
class ChineseTests(unittest.TestCase):
 def test_chinese_preview_and_strict(self):
  d=studio.new();d['pages'][0]['elements'][0]['text']='欢迎使用';im,issues=studio.render(d)
  self.assertFalse(any(i['type']=='missing' for i in issues));self.assertTrue(im.getbbox())
  d['font_mode']='firmware';_,strict=studio.render(d);self.assertTrue(any(i['type']=='missing' for i in strict))
 def test_chinese_variable_and_name(self):
  d=studio.new();d['variables']['温度']=25;d['pages'][0]['elements'][0]['text']='温度：{温度}';studio.validate(d);_,issues=studio.render(d)
  self.assertFalse(any(i['type'] in ('variable','missing') for i in issues));self.assertEqual(core.draft_path('project_中文测试').name,'project_中文测试.json')
  with self.assertRaises(ValueError):core.draft_path('../中文')
 def test_dialog_and_unsupported(self):
  d=studio.new();e=studio.element('dialog');e['id']='dialog';d['pages'][0]['elements']=[e];d['active_dialog']='dialog';_,issues=studio.render(d);self.assertFalse(any(i['type']=='missing' for i in issues))
  self.assertIsNone(chinese_font.rows('🦊'))
if __name__=='__main__':unittest.main(verbosity=2)

import copy,sys,tempfile,unittest
from pathlib import Path
import core

class Tests(unittest.TestCase):
    def test_actual_firmware_frames(self):
        d=core.defaults();d['simulation'].update(key=4,enc=-9999,raw=4095,avg=4095,light_ok=True,imu_ok=True,ax=-32768,ay=-32768,az=32767,id=112,samples=99999,errors=99999,servo_on=False,pulse=1500)
        for i in range(4):
            image,issues=core.render(d,i)
            raw=(core.FIRMWARE/'Previews'/f'page{i+1}.bin').read_bytes()
            diff=sum(image.getpixel((x,y))!=bool(raw[(y//8)*128+x]&(1<<(y%8))) for y in range(64) for x in range(128))
            self.assertEqual(diff,0, f'page {i+1} differs by {diff} pixels')
            self.assertEqual(issues,[])
    def test_missing_overflow(self):
        d=core.defaults();d['pages'][0][0].update(text='🦊',x=125,y=60)
        _,issues=core.render(d,0)
        self.assertEqual({x['type'] for x in issues},{'missing','overflow'})
    def test_dynamic_input(self):
        d=core.defaults();d['simulation'].update(raw=123,avg=456,ax=-200,ay=150,az=16000,imu_ok=True)
        self.assertEqual(core.element_text(d['pages'][1][1],d['simulation'],d['alternatives']),'RAW:123 AVG:456')
        self.assertIn('-200',core.element_text(d['pages'][2][1],d['simulation'],d['alternatives']))
        self.assertNotEqual(core.render(d,1)[0].tobytes(),core.render(core.defaults(),1)[0].tobytes())
    def test_save_revision(self):
        with tempfile.TemporaryDirectory() as tmp:
            old=core.DRAFTS;core.DRAFTS=Path(tmp)
            try:
                first=core.load('default');second=copy.deepcopy(first);first['ideas']='一个新想法'
                result=core.save('default',first,0);self.assertEqual(result['revision'],1)
                with self.assertRaises(RuntimeError):core.save('default',second,0)
                self.assertEqual(core.load('default')['ideas'],'一个新想法')
                with self.assertRaises(ValueError):core.load('../bad')
            finally:core.DRAFTS=old

    def test_model_fingerprint_does_not_silently_refresh(self):
        d=core.defaults();original=core.source_hash
        try:
            core.source_hash=lambda:core.MODEL_SOURCE_HASH
            self.assertFalse(core.source_changed(d))
            core.source_hash=lambda:'changed firmware'
            self.assertTrue(core.source_changed(d))
            self.assertTrue(core.source_changed(core.defaults()))
        finally:core.source_hash=original

    def test_state_text_is_independent(self):
        d=core.defaults();s=d['simulation'];alt=d['alternatives']
        for page,kind,flag,alternate in [(1,'light_hint','light_ok','light_bad'),(2,'imu_status','imu_ok','imu_bad'),(3,'servo_status','servo_on','servo_on')]:
            e=next(e for e in d['pages'][page] if e['kind']==kind)
            alt[alternate]='CHANGED';s[flag]=page==3
            self.assertEqual(core.element_text(e,s,alt),'CHANGED')
            s[flag]=not s[flag]
            self.assertEqual(core.element_text(e,s,alt),e['text'])

if __name__=='__main__':unittest.main(verbosity=2)

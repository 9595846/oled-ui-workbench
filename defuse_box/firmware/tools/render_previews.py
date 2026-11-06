from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
root=Path(__file__).resolve().parents[1]
canvas=Image.new('RGB',(1100,700),'#edf2f7')
draw=ImageDraw.Draw(canvas)
font=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',24)
names=['按键与旋钮检查','光敏原始值与滤波值','IMU 身份与采样计数','舵机空载调试（默认关闭）']
for i in range(4):
    data=(root/f'Previews/page{i+1}.bin').read_bytes()
    im=Image.new('RGB',(128,64),'black')
    for y in range(64):
        for x in range(128):
            if data[(y//8)*128+x] & (1<<(y%8)): im.putpixel((x,y),(255,255,255))
    im=im.resize((512,256),Image.Resampling.NEAREST)
    x=25+(i%2)*550;y=20+(i//2)*345
    draw.text((x,y),names[i],font=font,fill='#172d40')
    canvas.paste(im,(x,y+45))
canvas.save(root/'Previews/基础诊断页面.png')
print('Rendered actual firmware framebuffer with simulated values, not a board photo.')

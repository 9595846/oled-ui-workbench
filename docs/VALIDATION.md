# 验证与复现

发布目录保持固件源码和 Project.uvprojx 的原始字节，以保证 export_profile.json 中的指纹可复核。Keil 的 .uvoptx 为本机配置，未提交；编码修复脚本已兼容该文件缺失。

在仓库根目录运行：

```powershell
# 先用 GCC 生成原始帧缓冲，供 test_core 逐像素比较。
./defuse_box/firmware/tools/test_base.ps1
./oled_preview/.venv/Scripts/python.exe -m unittest discover -s oled_preview -p "test_core.py"
./oled_preview/.venv/Scripts/python.exe -m unittest discover -s oled_preview -p "test_studio.py"
./oled_preview/.venv/Scripts/python.exe -m unittest discover -s oled_preview -p "test_chinese.py"
./oled_preview/.venv/Scripts/python.exe oled_preview/test_http.py
./oled_preview/.venv/Scripts/python.exe oled_preview/test_mcp.py
./oled_preview/.venv/Scripts/python.exe oled_preview/test_exporter.py
./defuse_box/firmware/tools/test_base.ps1
./defuse_box/firmware/tools/build_keil.ps1
```

导出测试需要 GCC 在 PATH，ARMCC 检查默认使用 E:/keil5/ARM/ARMCC/bin/armcc.exe。Keil 构建脚本支持 -Uv4 参数指定安装位置；主机固件测试支持 -Gcc 参数。不要把工具未安装造成的跳过理解为通过。

本次集成已通过完整 Keil 编译/链接、保护逻辑回归和第五页逐像素比较；未连接硬件进行烧录验收。历史工作台测试记录见 oled_preview/VERIFICATION.md、STUDIO_GUIDE.md，其中旧阶段“未导出/未编译”的描述仅对应当时阶段，以根 README 当前集成状态为准。

# 第五页导出界面接入与验收

来源：oled_preview/exports/project_my_oled，设计 SHA256：1b38f34bca5fa3c530562478487c4d9ba2a1171b2c8cc91f12385f2995faa2d6。
当前设计仅在 (38,4) 显示“主页面”，没有图片或按键动作。

## 接入方式
- 沿用本目录 Project.uvprojx，目标 Defuse_Base，不改变芯片、库、编译器或引脚配置。
- 新增 Hardware/ui_assets、ui_pages、ui_actions 六个 C/H 文件；三个源文件已加入工程。
- User/main.c 初始化导出 UI，第五页使用 ui_draw；前四页保持原绘制和后台任务。
- KEY4 (PB9) 保留为全局翻页键，循环五页；PAGE 命令支持 1..5。
- 当前导出没有交互绑定，所以本阶段未把实体按键和旋钮交给 ui_event；以后添加交互时需单独协调 KEY4 的退出行为。
- 未绑定 value 到任何传感器或舵机，也没有新增硬件动作。
- 离开舵机页面仍立即关闭舵机输出，15 秒闲置保护保留。

## 已执行验证
- 主机回归测试通过，包括新增第五页进入/退出、非法 PAGE 6、舵机保护。
- 实际 C 绘制的第五页 8192 像素与导出设计逐像素一致。
- Keil 完整 Rebuild + 链接 + HEX 生成：0 Error(s), 0 Warning(s)。
- 编译器 ARMCC V5.06 update 7 (build 960)。
- Code=11558, RO-data=2902, RW-data=152, ZI-data=6376 字节。
- Flash 合计约 14612 字节；RAM 合计 6528 字节，在 STM32F103C8 容量内。
- 编译日志：BuildLogs/Keil_Defuse_Base.log；HEX：release/Defuse_Base.hex。
- 尚未烧录或完成实体 OLED 验收。

## 你烧录后的检查顺序
1. 打开本目录 Project.uvprojx，确认目标 Defuse_Base，沿用已配置的 ST-Link 下载。
2. 下载成功后复位，启动页仍为原来的按键旋钮检查页。
3. 每次短按并松开 KEY4 (PB9)：光敏 → IMU → 舵机 → 新主页面。
4. 第五页应只有“主页面”三个字，起点 X=38、Y=4；此页按 KEY1～KEY3 不应启动舵机。
5. 再按 KEY4 返回第一检查页。确认原有传感器、旋钮显示仍工作。
6. 串口 115200 8N1 发送 PAGE 5，再发送 STATUS，预期 PAGE=5；PAGE 1 可返回。
7. 需要测试舵机时，在原舵机页按已有步骤启动，再按 KEY4 切到第五页，确认停止输出；不要用保持力判断转动命令是否停止。
8. 将显示照片和异常现象反馈后，再进入下一阶段。

## 后续维护
继续导出到同一个工作台目录，核对后更新上述生成文件，不覆盖硬件业务代码。工作台 export_profile.json 已同步本次核对后的工程指纹，仍会拒绝未经复核的工程变化。

# 两个工作台的桌面套装与联动

套装与启动器的主体维护在 **[9595846/wiring-workbench](https://github.com/9595846/wiring-workbench)**。

- [套装使用与源码构建](https://github.com/9595846/wiring-workbench/blob/main/docs/SUITE.md)
- [OLED 设计绑定与预览联动](https://github.com/9595846/wiring-workbench/blob/main/docs/OLED_LINK.md)
- [启动器背景、原创图标及生成提示词](https://github.com/9595846/wiring-workbench/tree/main/assets/launcher)

套装支持独立打开接线/OLED 软件、分目录保存、通过已保存设计联动，以及请求正常关闭本套装的两个软件。关闭功能不强制结束进程，保留保存和退出提示。移动整个套装后，内部相对路径仍可使用。

本 OLED 仓库继续保留独立编辑器及其原有说明。主仓库的 `oled_companion/` 是套装配套版本，来源于本项目并合入桌面联动兼容改动，不宣称与这里的 main 逐文件一致，也不会自动覆盖这里的源码。

本轮在本仓库只补充文档，套装代码和视觉资源放在主仓库。生成的 EXE/ZIP、个人草稿、请求、历史、本机路径和桌面快捷方式不提交到源码仓库；按主仓库说明可在 Windows 构建。

套装中的数据是构建时已保存快照，与原独立软件不自动同步。两端未保存内容不会进入联动预览；不编译、烧录或自动修改 Keil 工程。

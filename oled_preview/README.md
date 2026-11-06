# OLED 工作台使用说明

本工具用于 `defuse_box/firmware` 的四个基础检查页面：按键旋钮、光敏、IMU 和舵机。网页与 MCP 共用 `oled_preview/drafts/` 中的 JSON 草稿。基础检查页用于电脑预览；通用工作台另支持导出待审阅 C 文件（见 STUDIO_GUIDE.md）。不连接串口、不驱动舵机、不自动修改 Keil 工程、不编译或烧录。

## 打开工作台

在本目录双击 `start_editor.cmd`。命令窗口会显示本次的 `http://127.0.0.1:端口/` 并打开默认浏览器。端口每次可能变化；请使用这次窗口显示的地址，不要直接双击 `web/index.html`。

关闭网页不会停止服务；用命令窗口的 Ctrl+C 停止。需要更新 Python 服务代码时，关闭旧服务再启动；仅更新网页文件时刷新即可。

当前电脑已验证的解释器是 `C:\work\oled-ui-workbench\oled_preview\.venv\Scripts\python.exe`。命令行也可这样启动：

```powershell
Set-Location 'C:\work\oled-ui-workbench\oled_preview'
python -X utf8 server.py
```

依赖：Python 3.10+、Pillow；MCP 另外需要官方 `mcp` Python SDK。当前目录的 `vendor` 是之前安装的本地 SDK 依赖，不提交 Git。换电脑或依赖不可访问时，可在本目录创建虚拟环境：

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -X utf8 server.py
```

只用网页时不需要先连接 MCP。启动器优先使用本目录的 `.venv`，没有时使用 PATH 中的 Python。

## 编辑一页

1. 左侧选页面；窄窗口中页面按钮在上方。
2. 点击 OLED 上的文字，或使用“页面元素”下拉框选中一项。
3. 编辑当前状态的文字、X 和 Y。左上角是 `(0,0)`，往右 X 增加，往下 Y 增加。
4. 可以拖动选框、点击方向按钮；屏幕获得焦点后，方向键移动 1 像素，Shift+方向键移动 8 像素。
5. “撤销 / 重做”保留本次打开后的最多 100 步记录。在非输入框中，也可使用 Ctrl+Z / Ctrl+Y；输入框内保留浏览器自己的文字撤销。
6. “恢复当前页原始内容”只恢复该页的文字、位置及备用状态文字，保留其他页、便签和模拟数值；此操作可撤销，需保存才写入草稿。

动态数字不能当固定文字修改：例如 AX、RAW、脉宽由模拟参数产生。对“IMU 正常 / 异常”“舵机开启 / 停止”等状态，编辑框显示当前状态的文字；切换模拟状态后可编辑另一段文字。

中文使用工程现有 12 像素字模，ASCII 使用工程实际绘制规则，包含固件的小写转大写行为。缺字保留在草稿并提示，不自动补字。屏幕上的方框是缺字提示，不能当成实体 OLED 支持该字的证据。缺字与越界提示可点击，定位相应元素。越界内容会按屏幕边界裁切。

## 模拟操作

| 操作 | 预览行为 |
| --- | --- |
| KEY1～KEY3，在前三页 | 记录按键编号；按键旋钮页能看到编号 |
| KEY4 | 下一页；停止模拟舵机 |
| 舵机页 KEY1 | 开启 / 停止，开启时回到 1500 μs |
| 舵机页 KEY2 | 停止 |
| 舵机页 KEY3 | 显示模拟提示音事件，不实际播放或控制蜂鸣器 |
| 左转 / 右转 | 旋钮计数变化；舵机页开启时，每格调整 10 μs，限制在 1400～1600 μs |
| 15 秒不调整舵机 | 自动停止；重新打开保存为“开启”的草稿时，从打开时间重新计 15 秒 |
| 侧栏切换页面 | 与程序换页一致，停止模拟舵机 |

“传感器模拟参数”可输入 RAW/AVG、AX/AY/AZ 和 ID，并切换正常 / 异常。ID 输入为十进制，例如 112 对应屏幕的 70（十六进制）。这是手工输入的模拟值，不是实时采样，也不是完整传感器模型。采样计数、错误计数仍是草稿数值，不随真实时间自动增长。

## 便签、保存与冲突

便签可记录：触发条件 → 屏幕变化 → 玩家操作 → 验收现象。例如“环境变暗后隐藏密码；旋钮转对方向才显示下一位”。便签随保存草稿一起保存，没有自动保存。

- 点击“保存草稿”或 Ctrl+S。名称只用英文字母、数字、下划线、短横线，最长 40 字符。
- 修改名称后保存到一个未使用的新名称，可另存副本。若新名称已经存在，则拒绝覆盖，需先打开它或换名。
- 输入已保存名称后点“打开草稿”。有未保存修改会先确认。名称不存在时会明确提示并载入原始页面，直到保存才创建文件。
- MCP 或另一个浏览器窗口保存后，当前窗口不会自动覆盖自己的编辑。保存遇到版本冲突会保留本地内容；换名另存，或点击打开重新读取最新版本。
- 保存中的新编辑不会丢失，会继续标记为未保存。
- 撤销记录仅在当前窗口内存中，重新打开后清空；JSON 草稿不是版本历史仓库。
- “导出 PNG”保存当前页的 128×64 原始像素，不含编辑选框。渲染尚未完成时按钮不可用，避免导出旧画面。

源文件指纹与已经核对过的页面模型绑定。固件显示代码、字库等发生变化后，会提示重新核对模型；不能仅点恢复页面就把差异当作已解决。

## 连接 MCP

服务使用本地 **stdio**。请在支持 MCP 的客户端提供下列启动参数；这是参数示例，不会自动修改任何全局配置。

```json
{
  "command": "C:\\work\\oled-ui-workbench\\oled_preview\\.venv\\Scripts\\python.exe",
  "args": [
    "-X", "utf8",
    "C:\\work\\oled-ui-workbench\\oled_preview\\mcp_server.py"
  ]
}
```

若使用虚拟环境，把 command 改成本目录 `.venv\Scripts\python.exe` 的绝对路径。不同客户端的配置外层格式可能不同，以上仅是进程命令和参数。stdio 服务没有需要在浏览器打开的 MCP URL。

| 工具 | 参数 / 作用 |
| --- | --- |
| `read_pages` | 无参数；读取原始四页模型，含源文件摘要 |
| `read_draft` | `name`，默认 `default`；读取草稿及 revision |
| `update_draft` | `name`、完整 `draft`、`expected_revision`；按修订号保存 |
| `export_ui` | `name`、`expected_revision`；导出已保存通用草稿 |
| `inspect_preview` | `name`；当前页 PNG base64、缺字、越界及源文件变化提示 |

建议给 AI 这样说：

> 先用 read_draft 读取 default 草稿，只修改第一页标题的位置与便签。保留其他字段，用读取到的 revision 作为 expected_revision 保存，然后用 inspect_preview 检查缺字和越界。遇到冲突先重新读取，不直接覆盖别人的修改。不修改 Keil 工程。

网页和 MCP 不必同时启动，也可以同时使用；只共享已保存草稿。网页上尚未保存的内容，MCP 无法看到。源目录和草稿目录由本项目固定，工具不接受任意文件路径。

## 文件与验证

- `web/`：界面和浏览器模拟行为。
- `core.py`：字库解析、像素渲染、草稿验证、文件锁和修订号。
- `server.py`：仅监听 127.0.0.1 的网页服务。
- `mcp_server.py`：官方 Python SDK stdio 服务。
- `drafts/`：个人草稿，已忽略 Git。
- `verification/`：本次截图、PNG、浏览器验证脚本、固件哈希证据。
- `VERIFICATION.md`：实际测试结果与未验证事项。

在项目根目录可运行：

```powershell
python -X utf8 oled_preview/test_core.py
python -X utf8 oled_preview/test_http.py
python -X utf8 oled_preview/test_mcp.py
node --check oled_preview/web/app.js
```

验收边界：电脑上的像素比较、浏览器操作、MCP 测试不能代替 Keil 编译和实体 OLED 验收。应用草稿到固件是后续单独步骤，需你确认之后再修改现有工程。

通用项目编辑、弹窗、图片和预设的新功能，请阅读 [通用编辑器说明](STUDIO_GUIDE.md)。从原工作台顶部的“通用编辑器”进入；服务更新后需重新启动。

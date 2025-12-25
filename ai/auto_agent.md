# 2025盘点自动化 AI agent 与工作原理

2025年是自动化AI Agent爆发的一年，许多开源的自动化 AI agent 层出不穷。本文我们就进行盘点，并将它们按照 **网页端 (Web)**、**移动端 (Mobile)** 和 **桌面端 (Desktop)** 进行分类，以及分析一下他们的底层原理。

## AI Agent 开源项目对比表

| 项目名称 | 主要环境 | 感知方式 | 主要语言 | 核心优势 |
| --- | --- | --- | --- | --- |
| **Browser-use** | 浏览器 | 视觉 + DOM | **Python** | 社区热度极高，支持 Playwright 联动，适配几乎所有主流 LLM。 |
| **Skyvern** | 浏览器 | 视觉 + DOM | **Python** | 专注于复杂商业流程自动化，具备处理验证码和动态 UI 的稳定性。 |
| **Firecrawl** | 网页 / API | DOM 解析 | **TypeScript** | 专注于将网页清洗为 LLM 易读的 Markdown，为其他 Agent 提供数据。 |
| **Midscene.js** | 浏览器 | 视觉 + JSON | **TypeScript** | 专为前端自动化测试设计，支持用自然语言编写测试脚本。 |
| **Page-agent** | 浏览器 | DOM / 视觉 | **TypeScript** | 轻量化，通常作为浏览器插件运行，适合个人用户的简单网页任务。 |
| **OWL Agent** | Web / 终端 | 视觉 + 协议 | **Python** | 基于 CAMEL-AI，支持 MCP 协议，擅长多 Agent 协作处理跨网页和跨终端的任务。 |
| **Open Operator** | 浏览器 | 视觉 + DOM | **Python** | 由 Browserbase 维护，旨在成为 OpenAI "Operator" 的开源替代品，侧重于浏览器操作。 |
| **MobileAgent** | 安卓手机 | 纯视觉 | **Python** | 阿里出品，不依赖底层元数据，直接通过截图识别图标，视觉精度极高。 |
| **OMG-Agent** | 安卓手机 | 视觉 + UI 树 | **Python** | 针对长程任务优化，在大规模 App 环境中执行更稳定。 |
| **Open-AutoGLM** | 手机 / Web | 视觉 + 语义 | **Python** | 中文适配极佳，针对国内主流 App 和网页深度优化。 |
| **auto-wing** | 手机 / Web | DOM解析 | **Python** | 支持主流的国内模型，适合 App 和 Web 自动化测试。 |
| **Mobile-Agent-v3** | 手机 / 跨平台 | 视觉 (GUI-Owl) | **Python** | 阿里 X-PLUG 团队最新作。基于自研模型 GUI-Owl，在异常处理（弹窗、广告）和长程任务上极强。 |
| **OpenPhone** | 手机 (端侧) | 视觉 | **Python** | **轻量化标杆**。首个 3B 参数量的端侧手机 Agent 模型，强调隐私和零 API 成本，可在手机本地运行。 |
| **Microsoft UFO** | Windows | 视觉 + UI Tree | **Python** | 微软官方出品，擅长跨 Windows 应用联动（如 Office 协作）。 |
| **Self-Operating** | 全系统桌面 | 视觉 (截图) | **Python** | 模仿人类操作键鼠，不依赖底层代码，支持任何操作系统环境。 |
| **Open Interpreter** | 桌面端 (OS) | 代码执行 / 视觉 | **Python** | **顶级热门**。通过本地执行代码控制键鼠和系统。其“本地化”和“全权限”是最大卖点。 |
| **Bytebot** | Linux 桌面 | 视觉 + DOM | **Python / TS** | 提供容器化的虚拟桌面环境，专门为 AI 提供一个“办公室”，适合在云端运行桌面任务。 |
| **Goose** | 桌面端 (Dev) | 代码 + 终端 | **Rust / TS** | Block (原 Square) 出品。定位为超越代码补全的“工程 Agent”，能直接安装、编辑、测试整个项目。 |
| **smolagents** | 框架 / 综合 | Actionable API | **Python** | Hugging Face 出品。极简轻量，通过编写短小的 Python 函数（Code Actions）来执行任务，逻辑极其清晰。 |

当然，AI Agent 不止于上面这个表格所罗列的，相信你还能找出很多。

这些 AI Agent 本质上是自动化，作为一名测试工程师，在刚入行时就会接触到自动化测试，当我们用 `selenium`/ `playwright`/ `appium` 等写好了一段话脚本，看着他在操作浏览器、App 执行，一开始是兴奋的，作为工作多年的测试工程师，其实是比较麻木的。改变的仅仅只是输入行为：selenium IDE录制回放、sikuli的脚本加截图、selenium webdriver写定位操作。AI agent只是把输入形式换成了自然语言。由于他以极低的门槛走向了普通用户，引起了更多人的关注和使用。用粉丝文化叫做“出圈“了。

## 自动化 AI Agent工作原理

静下心来，这么多AI agent的识别能力（感知方式）核心就三类：

* 纯视觉
* DOM 解析
* 视觉 + DOM/JSON/UI Tree/语义

是三种方案的底层原理深度解析：

### 1. 纯视觉方案 (Pure Vision / Pixel-to-Action)

这种方案将屏幕视为一张纯粹的图片，完全不读取底层代码（如 HTML 或 XML）。

* **核心逻辑：**
1. **截图 (Capture)：** 定时截取当前屏幕图像。
2. **视觉感知 (Perception)：** 将图片输入多模态大模型（VLM，如 GPT-4o-vision 或 Qwen-VL）。模型通过视觉特征识别出按钮、输入框、图标。
3. **坐标映射 (Grounding)：** 这是最关键的一步。模型需要输出点击位置的像素坐标 。为了提高精度，通常会对图片加装“坐标网格（Grid）”或使用特定的视觉定位模型。
4. **动作执行 (Execution)：** 调用系统级 API（如 Python 的 `pyautogui` 或安卓的 `adb tap`）直接点击对应的坐标点。

### 2. DOM 解析方案 (DOM / Tree-based)

这种方案主要用于 Web 环境，它认为“代码即真相”。

* **核心逻辑：**
1. **提取树结构 (Extraction)：** 获取网页的 DOM Tree。
2. **树简化 (Simplification)：** 原始 DOM 极其庞大（动辄几万行），超出了模型的上下文（Context Window）。Agent 会剔除无关的脚本、样式表和冗余标签，只保留 `button`, `a`, `input` 等交互元素。
3. **赋予标识符 (Tagging)：** 给每个关键元素打上一个唯一的 ID（例如 `[ID=12] 登录按钮`）。
4. **逻辑推理 (Reasoning)：** 将简化后的文本/Markdown 传给 LLM。模型回答：“我应该点击 ID=12 的元素”。
5. **动作执行：** 通过 `playwright.click('selector')` 精确操作 DOM 节点。


### 3. 混合方案 (Vision + Semantic/DOM/UI Tree)

* **核心逻辑：**

1. **多模态输入：** 同时将 **屏幕截图** 和 **UI 结构信息（Accessibility Tree / DOM / JSON）** 喂给模型。
2. **对齐 (Alignment)：** 模型通过视觉确认“这个看起来像搜索框”，同时通过 UI Tree 确认“这个元素的底层 ID 是 SearchInput”。
3. **语义理解：** 比如在手机端，方案会利用 **无障碍服务 (Accessibility Service)** 提取每个控件的语义描述（Label）。即使界面变了，只要语义标签（如“提交”）没变，Agent 就能定位。
4. **反馈循环 (Self-Correction)：** 执行动作后再次截图，对比前后变化。如果视觉上发现弹窗没消失，说明点击失败，立即进行纠错。

## 如何进一步提升AI agent的识别能力？

### 1. Web 端：从“海量 DOM”到“精简语义”

Web 页面动辄上万个 DOM 节点，直接喂给大模型会由于 **Token 溢出** 和 **噪声干扰** 导致识别失败。以 `Browser-use` 和 `Midscene.js` 为代表的项目核心优化点在于：

* **DOM 蒸馏与精简 (DOM Distillation)：**
  * **底层技术：** 递归遍历 DOM 树，剔除所有不可见元素（`display: none`, `opacity: 0`）、非交互元素（大量的样式容器 `div`）以及冗余属性（`class`, `style`）。
  * **提升点：** 将数万行的 HTML 压缩成几百行的 **Markdown** 或 **JSON**。模型不再看原始代码，而是看一个“纯净的交互列表”。

* **交互元素打标 (Interactive Element Tagging)：**
  * **底层技术：** 自动给每一个 `<a>`、`<button>`、`<input>` 标签分配一个临时的、唯一的数字 ID（例如 `[12] 搜索框`），并在截图上通过覆盖层（Overlay）把这些 ID 标注出来。
  * **提升点：** 模型在思考时只需说“点击 ID 为 12 的元素”，避开了复杂的 XPath 或 Selector 编写，极大提高了操作的精准度。

* **利用 AOM (Accessibility Object Model)：**
  * **底层技术：** 不直接读取 HTML，而是读取浏览器内部生成的 **无障碍树**。
  * **提升点：** 无障碍树本身就是为“盲人读屏软件”设计的，它已经自动过滤了装饰性内容，只保留了具有“语义”的控件，天然适合 AI 理解。


### 2. 手机端：从“坐标盲点”到“结构补全”

安卓手机端没有像网页那样规范的 DOM，它的 UI 结构（XML）经常缺失关键信息。`Open-AutoGLM` 和 `MobileAgent` 主要攻克以下技术细节：

* **UI 层次结构转义 (UI Hierarchy Parsing)：**
  * **底层技术：** 通过 ADB 获取 `uiautomator dump` 生成的 XML 文件。由于很多安卓控件没有 `text`（例如纯图片图标），Agent 会通过**视觉模型 (VLM)** 为这些空控件自动“贴标签”。
  * **提升点：** 解决了“点击购物车图标”的问题——即使 XML 里没有“购物车”这个词，视觉模型也能在图中识别出它是购物车，并将其与 XML 中的节点对应。

* **坐标归一化与对齐 (Coordinate Grounding)：**
  * **底层技术：** 将屏幕像素坐标（如 1080x2400）映射到  的相对坐标系，并强制模型输出在该坐标系内的点击点。
  * **提升点：** 这种“归一化”技术让模型对不同尺寸、不同分辨率的手机具有很强的迁移性，不会因为屏幕换了就点偏。

* **多模态融合决策 (Multimodal Fusion)：**
  * **底层技术：** `Open-AutoGLM` 并不是只看图或只看代码，而是将 **“当前截图 + 上一步动作 + 当前 XML 片段”** 同时输入模型。
  * **提升点：** 这类似于给 AI 装上了“眼睛”和“触觉”。如果图片显示有广告遮挡，即使 XML 说按钮在那，AI 也会先选择关闭广告。


### 核心技术对比：Web vs Mobile

| 提升维度 | Web 端 (如 Browser-use) | 手机端 (如 Open-AutoGLM) |
| --- | --- | --- |
| **定位精度** | 依靠 **CSS/XPath 选择器**，精度达像素级。 | 依靠 **VLM 输出坐标** + ADB 模拟点击。 |
| **语义来源** | HTML 标签、ARIA 属性、DOM ID。 | XML 结构、OCR 识别、图标视觉特征。 |
| **处理难题** | 动态加载、IFrame 嵌套、影子 DOM。 | 系统弹窗拦截、手势滑动（Swipe）模拟。 |
| **自愈能力** | 页面刷新后重新获取 DOM 树进行匹配。 | 每次动作后重新截图，对比界面变化（Diff）。 |

## 最后

当我们了解了上面的原理，DOM 解析的本质是转化为 **CSS/XPath 选择器**， 视觉识别的本质是转化为 **坐标** ，其实这些自动化 AI agent的核心能力是来源于LLM模型的能力，AI agent的将这些 LLM 进行包装，提供更简单的功能，更简单的 API 或者是浏览器插件给到用户使用。

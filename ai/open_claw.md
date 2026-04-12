# 揭秘OpenClaw：AI助手的“魔法”其实是代码

有人说：啥都能干，有人说 啥也干不了，有人说：妥妥智商税，有人说：未来以来。

甚至，我媳妇不搞技术，她天天催着我搭建openclaw的，赶紧用起来，然后，又一再强调不要在本地搭建，即视作未来助手，有视作洪水猛兽。真这么牛逼又可怕吗？

OpenClaw 并没有什么神奇的地方。它本质上是一个基于大语言模型（LLM）的编程框架，通过简单的 Python 代码调用 API 接口，实现各种功能。底层原理就是利用现有的 AI 模型（如通义千问），结合编程逻辑来扩展能力。没有魔法，只有代码和算法。以下通过一系列示例，逐步解密其“神奇”之处，从基础的 API 调用开始，到添加记忆、文件操作、定时任务和联网检索，每一步都展示如何通过代码实现看似复杂的 AI 助手功能。

## 示例1: 基础对话：直连大模型API，无记忆的简单交互

这个示例展示了最基础的 OpenClaw 使用：直接调用大模型 API 进行对话。代码使用 OpenAI 兼容的客户端库，连接到阿里云的 DashScope 服务，发送用户输入并流式接收回复。

运行结果显示，LLM 本身没有记忆能力，每次对话都是独立的，没有上下文。这是因为代码中每次只发送当前消息，不保留历史记录。底层原理很简单：API 调用是无状态的，记忆需要开发者手动管理。

```python
from openai import OpenAI
import os

client = OpenAI(
    # 如果没有配置环境变量，请用阿里云百炼API Key替换：api_key="sk-xxx"
    api_key=os.getenv("DASHSCOPE_API_KEY", "sk-xxx"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

while True:
    msg = input("\n你：")

    # 每次只发送当前消息，不保留历史记录
    messages = [{"role": "user", "content": msg}]
    completion = client.chat.completions.create(
        model="qwen3.5-plus",
        messages=messages,
        extra_body={"enable_thinking": False},
        stream=True
    )

    is_answering = False
    for chunk in completion:
        delta = chunk.choices[0].delta
        if hasattr(delta, "reasoning_content") and delta.reasoning_content is not None:
            if not is_answering:
                print(delta.reasoning_content, end="", flush=True)
        if hasattr(delta, "content") and delta.content:
            if not is_answering:
                print("\n" + "-" * 20 + "完整回复" + "-" * 20)
                is_answering = True
            print(delta.content, end="", flush=True)
    print("\n" + "=" * 50)  # 分隔线，区分不同问答回合

```

运行结果 LLM 并无记忆能力：


```shell
你：1+1等于几？

--------------------完整回复--------------------
在基础的算术运算中，**1 + 1 等于 2**。

这是自然数加法的基本规则：当你有一个单位，再增加一个相同的单位时，总共会有两个单位。

*注：在某些特定的语境（如二进制计算机逻辑）中，1 + 1 可能表示为 `10`；而在脑筋急转弯或特定比喻中，答案可能会不同，但在标准数学定义下，答案始终是 **2**。
==================================================

你：再加1

--------------------完整回复--------------------
好的，现在是 **2**。

如果您是在进行连续计数或需要基于某个特定数值继续累加，请告诉我当前的上下文，我会为您准确计算！
==================================================
```

## 示例2: 对话记忆：让AI记住上下文的简单技巧

在这个示例中，我们通过维护一个 `messages` 列表来存储对话历史，每次调用 API 时将整个历史传递给模型，从而实现对话记忆。底层原理是利用 LLM 的上下文窗口能力，将历史消息作为输入的一部分。没有神奇的持久存储，只是简单的列表操作。

运行结果显示，LLM 现在能读取对话记录，正确理解“再加1”是指基于之前的“1+1=2”继续计算。

```python
from sample.ai_utils import create_client, stream_chat_response, is_exit_command

client = create_client()
messages = []  # 用于存储对话历史

while True:
    msg = input("\n你：")

    # 将当前用户消息添加到历史记录
    messages.append({"role": "user", "content": msg})

    completion = client.chat.completions.create(
        model="qwen3.5-plus",  # 您可以按需更换为其它深度思考模型
        messages=messages,
        extra_body={"enable_thinking": False},
        stream=True
    )

    is_answering = False  # 是否进入回复阶段
    # 收集完整的回复内容
    full_response = ""

    full_response = stream_chat_response(completion, title="完整回复")

    # 将AI的回复添加到历史记录
    messages.append({"role": "assistant", "content": full_response})

    print("\n" + "=" * 50)  # 分隔线，区分不同问答回合
    print(f"当前对话轮数：{len(messages) // 2}")  # 显示当前对话轮数
```

运行结果（LLM读取对话记录）：

```shell
你：1+1等于几？

--------------------完整回复--------------------
在标准的算术运算中，**1 + 1 等于 2**。

这是最基础的数学事实：当你将一个单位与另一个相同的单位时，总共会得到两个单位。

*注：在某些特定的语境（如二进制计算机运算）中，1+1 的结果写作 `10`（代表十进制的 2）；而在一些脑筋急转弯或创意场景中，答案可能会有所不同，但在常规数学逻辑下，答案始终是 **2**。
==================================================
当前对话轮数：1

你：再加1

--------------------完整回复--------------------
承接上一步的结果（2），再加 1：

$$2 + 1 = 3$$

所以，结果是 **3**。
==================================================
当前对话轮数：2
```

## 示例3： 永久记忆助理：AI如何记住你的个人信息

这个示例进一步扩展记忆能力，通过 JSON 文件持久化存储用户信息。代码使用正则表达式提取用户输入中的记忆指令，并将其保存到本地文件。底层原理是结合文件 I/O 和文本解析，没有任何 AI 魔法，只是编程技巧。

运行示例展示了如何记住用户信息，并在后续对话中调用。

```python
from sample.ai_utils import create_client, stream_chat_response, is_exit_command
import os
import json
import re

client = create_client()

MEMORY_FILE = "assistant_memory.json"


def load_memory():
    """从文件加载永久记忆"""
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"加载记忆文件失败：{e}")
            return {}
    return {}


def save_memory(memory):
    """保存永久记忆到文件"""
    try:
        with open(MEMORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(memory, f, ensure_ascii=False, indent=2)
        print(f"💾 记忆已保存到 {MEMORY_FILE}")
        return True
    except Exception as e:
        print(f"保存记忆文件失败：{e}")
        return False


def extract_memory_from_text(text):
    """从文本中提取要记住的信息"""
    memory_info = {}

    # 多种记忆模式
    patterns = [
        r'记住[：:]\s*(.+?)(?:\n|$)',
        r'请记住[：:]\s*(.+?)(?:\n|$)',
        r'记忆[：:]\s*(.+?)(?:\n|$)',
        r'保存[：:]\s*(.+?)(?:\n|$)',
        r'帮我记住[：:]\s*(.+?)(?:\n|$)',
    ]

    for pattern in patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            # 解析记忆内容
            if '：' in match or ':' in match:
                # 键值对格式：姓名：张三
                parts = re.split('[：:]', match, 1)
                if len(parts) == 2:
                    key, value = parts
                    memory_info[key.strip()] = value.strip()
            else:
                # 自由文本格式，使用时间戳作为键
                import time
                key = f"note_{int(time.time())}"
                memory_info[key] = match.strip()

    return memory_info


def format_memory_for_prompt(memory):
    """将记忆格式化为提示词"""
    if not memory:
        return ""

    memory_text = "## 你记住的用户信息\n"
    memory_text += "以下是之前记住的用户信息，请记住并据此回答：\n"
    for key, value in memory.items():
        memory_text += f"- {key}: {value}\n"
    memory_text += "\n如果用户让你记住新信息，请回复确认。"
    return memory_text


# 加载永久记忆
permanent_memory = load_memory()
print("=" * 60)
print("🤖 AI 私人助理已启动")
print(f"📚 已加载 {len(permanent_memory)} 条永久记忆")
print("💡 提示：")
print("   - 说'记住：姓名 张三' 来保存信息")
print("   - 说'查看记忆' 查看所有记忆")
print("   - 说'忘记：姓名' 删除记忆")
print("   - 输入 'exit' 退出程序")
print("=" * 60)

messages = []  # 用于存储对话历史

while True:
    msg = input("\n你：").strip()

    # 退出命令
    if msg.lower() in ['exit', 'quit', '退出']:
        print("👋 再见！")
        break

    # 查看记忆命令
    if msg.lower() in ['查看记忆', '显示记忆', '我的记忆']:
        if permanent_memory:
            print("\n📚 永久记忆：")
            for key, value in permanent_memory.items():
                print(f"  • {key}: {value}")
        else:
            print("\n📭 暂无永久记忆")
        continue

    # 忘记命令
    if msg.lower().startswith('忘记：') or msg.lower().startswith('忘记:'):
        key_to_remove = msg.split('：')[-1].split(':')[-1].strip()
        if key_to_remove in permanent_memory:
            del permanent_memory[key_to_remove]
            save_memory(permanent_memory)
            print(f"🗑️ 已忘记：{key_to_remove}")
        else:
            print(f"❓ 未找到记忆：{key_to_remove}")
        continue

    # 处理用户输入中的记忆命令
    user_memory = extract_memory_from_text(msg)
    if user_memory:
        print(f"\n📝 检测到记忆请求，正在保存...")
        for key, value in user_memory.items():
            permanent_memory[key] = value
            print(f"  ✓ 记住：{key} = {value}")
        save_memory(permanent_memory)

    # 将当前用户消息添加到历史记录
    messages.append({"role": "user", "content": msg})

    # 构建包含永久记忆的完整消息列表
    memory_prompt = format_memory_for_prompt(permanent_memory)
    if memory_prompt:
        system_message = {"role": "system", "content": f"你是用户的私人助理。\n{memory_prompt}"}
        full_messages = [system_message] + messages
    else:
        full_messages = messages

    completion = client.chat.completions.create(
        model="qwen3.5-plus",
        messages=full_messages,
        extra_body={"enable_thinking": False},
        stream=True
    )

    print("\n" + "-" * 20 + "AI 回复" + "-" * 20)
    full_response = stream_chat_response(completion, title="AI 回复")

    # 检查AI回复中是否有需要记忆的内容
    ai_memory = extract_memory_from_text(full_response)
    if ai_memory:
        print(f"\n📝 AI 回复中包含记忆信息，正在保存...")
        for key, value in ai_memory.items():
            permanent_memory[key] = value
            print(f"  ✓ 记住：{key} = {value}")
        save_memory(permanent_memory)

    # 将AI的回复添加到历史记录
    messages.append({"role": "assistant", "content": full_response})

    print("\n" + "=" * 60)
    print(f"💬 对话轮数：{len(messages) // 2} | 📚 记忆条数：{len(permanent_memory)}")
```

运行示例：

```shell
加载记忆文件失败：Expecting value: line 1 column 1 (char 0)
============================================================
🤖 AI 私人助理已启动
📚 已加载 0 条永久记忆
💡 提示：
   - 说'记住：姓名 张三' 来保存信息
   - 说'查看记忆' 查看所有记忆
   - 说'忘记：姓名' 删除记忆
   - 输入 'exit' 退出程序
============================================================

你：记住：我的henry.hu ，一名测试工程师，经常需要学习新的测试技术和工具。

📝 检测到记忆请求，正在保存...
  ✓ 记住：note_1774455483 = 我的henry.hu ，一名测试工程师，经常需要学习新的测试技术和工具。
💾 记忆已保存到 assistant_memory.json

--------------------AI 回复--------------------
收到，我已经记住了：您是 **henry.hu**，一名**测试工程师**，经常需要学习新的测试技术和工具。

作为您的私人助理，如果您在探索新工具、寻找学习资源或制定技术提升计划时需要帮助，请随时告诉我！
============================================================
💬 对话轮数：1 | 📚 记忆条数：1

你：我是谁？

--------------------AI 回复--------------------
您是 **henry.hu**，一名**测试工程师**。

根据我之前记录的信息，您经常需要学习新的测试技术和工具。如果您需要推荐最新的技术栈、寻找学习资源或讨论测试方案，随时可以找我！
============================================================
💬 对话轮数：2 | 📚 记忆条数：1
```

## 示例4： 文件操作助手：AI如何操控本地文件系统

这个示例让 AI 能执行本地命令，通过 PowerShell 操作文件系统。代码使用 subprocess 调用系统命令，并解析 AI 的回复来决定执行什么。底层原理是利用操作系统接口，没有 AI 直接操作文件，只是通过代码桥接。

运行结果展示了如何创建文件。

```python
from sample.ai_utils import create_client, is_exit_command
import os
import subprocess
import re

client = create_client()

# 系统提示词，告诉AI使用PowerShell命令
system_prompt = """
你的目标是完成用户的任务，你必须选择下面的其中一种格式进行回复：
1. 如果你认为需要执行命令，则输出'命令：XXX'，XXX 为命令本身，不要用任何格式，不要解释
2. 如果你认为不需要执行命令，则输出'完成：XXX'，XXX 为你的总结信息

注意：当前系统是 Windows PowerShell，请使用 PowerShell 命令语法。
"""

messages = [{"role": "system", "content": system_prompt}]


def execute_command(command):
    """执行PowerShell命令"""
    try:
        result = subprocess.run(
            ["powershell", "-Command", command],
            capture_output=True,
            text=True,
            timeout=30,
            encoding='gbk',  # Windows中文系统默认是GBK编码
            errors='ignore'
        )

        if result.returncode == 0:
            output = result.stdout if result.stdout else "命令执行成功（无输出）"
            return f"执行结果：\n{output}"
        else:
            error_msg = result.stderr if result.stderr else "未知错误"
            return f"执行失败：\n{error_msg}"
    except Exception as e:
        return f"执行错误：{str(e)}"


def parse_and_execute(response_content):
    """解析AI回复，判断是否需要执行命令"""
    match = re.match(r'^命令[：:]\s*(.+)$', response_content.strip(), re.IGNORECASE)

    if match:
        command = match.group(1).strip()
        print(f"\n执行命令: {command}")
        result = execute_command(command)
        print(result)
        return result
    else:
        # 移除"完成："前缀
        display = re.sub(r'^完成[：:]\s*', '', response_content)
        print(f"\n{display}")
        return None


print("=" * 50)
print("AI Agent 已启动 (Windows PowerShell)")
print("输入 'exit' 退出")
print("=" * 50)

while True:
    msg = input("\n你：").strip()

    if msg.lower() in ['exit', 'quit', '退出']:
        break

    if not msg:
        continue

    messages.append({"role": "user", "content": msg})

    try:
        completion = client.chat.completions.create(
            model="qwen3.5-plus",
            messages=messages,
            extra_body={"enable_thinking": False},
            stream=False
        )

        full_response = completion.choices[0].message.content

        print("\n" + "-" * 50)
        result = parse_and_execute(full_response)

        if result:
            messages.append({"role": "assistant", "content": f"执行结果：\n{result}"})
        else:
            messages.append({"role": "assistant", "content": full_response})

        print("=" * 50)

    except Exception as e:
        print(f"\n错误: {str(e)}")
```

运行结果（）

```shell
==================================================
AI Agent 已启动 (Windows PowerShell)
输入 'exit' 退出
==================================================

你：创建 hello.py 文件，实现打印 hello world.

--------------------------------------------------

执行命令: Set-Content -Path "hello.py" -Value 'print("hello world")'
执行结果：
命令执行成功（无输出）
==================================================
```

## 示例5: 定时任务助手：AI如何帮你安排时间

这个示例使用 Python 的 threading 模块实现定时任务，通过正则表达式解析用户输入中的定时指令。底层原理是多线程和时间延迟，没有复杂的调度系统，只是简单的 sleep 和线程启动。

运行结果展示了定时提醒功能。

```python
from sample.ai_utils import create_client, stream_chat_response, is_exit_command
import threading
import time
import re

client = create_client()

# 存储定时任务
scheduled_tasks = []


def execute_scheduled_task(task_id, delay, command):
    """延迟执行任务"""
    time.sleep(delay)
    print(f"\n⏰ 定时任务执行: {command}")

    # 执行命令
    messages = [{"role": "user", "content": command}]
    completion = client.chat.completions.create(
        model="qwen3.5-plus",
        messages=messages,
        extra_body={"enable_thinking": False},
        stream=True
    )

    stream_chat_response(completion, title="定时回复")


def parse_schedule(msg):
    """解析定时任务"""
    # 匹配格式：5秒后 提醒我喝水
    pattern = r'(\d+)\s*(秒|分钟|小时)后\s*(.+)'
    match = re.match(pattern, msg)

    if match:
        num = int(match.group(1))
        unit = match.group(2)
        content = match.group(3)

        # 转换为秒
        if unit == '分钟':
            delay = num * 60
        elif unit == '小时':
            delay = num * 3600
        else:
            delay = num

        # 创建定时任务
        task_id = len(scheduled_tasks)
        thread = threading.Thread(
            target=execute_scheduled_task,
            args=(task_id, delay, content),
            daemon=True
        )
        thread.start()
        scheduled_tasks.append({"id": task_id, "thread": thread})

        return True, delay, content

    return False, 0, ""


print("=" * 60)
print("🤖 AI 助手已启动 (支持定时任务)")
print("📝 使用示例:")
print("   - 5秒后 提醒我喝水")
print("   - 2分钟后 查询天气")
print("   - 1小时后 叫我开会")
print("=" * 60)

while True:
    msg = input("\n你：").strip()

    if msg.lower() in ['exit', 'quit', '退出']:
        print("👋 再见！")
        break

    # 检查是否是定时任务
    is_schedule, delay, content = parse_schedule(msg)

    if is_schedule:
        print(f"✅ 已设置定时任务: {delay}秒后执行 '{content}'")
        continue

    # 普通问答
    messages = [{"role": "user", "content": msg}]
    completion = client.chat.completions.create(
        model="qwen3.5-plus",
        messages=messages,
        extra_body={"enable_thinking": False},
        stream=True
    )

    stream_chat_response(completion, title="完整回复")
    print("\n" + "=" * 50)
```


运行结果：

```shell
============================================================
🤖 AI 助手已启动 (支持定时任务)
📝 使用示例:
   - 5秒后 提醒我喝水
   - 2分钟后 查询天气
   - 1小时后 叫我开会
============================================================

你：5秒后 提醒我喝水
✅ 已设置定时任务: 5秒后执行 '提醒我喝水'

你：
⏰ 定时任务执行: 提醒我喝水

--------------------定时回复--------------------
💧 **喝水时间到啦！**

记得放下手头的工作，喝一口温水润润喉哦～保持身体水分充足，能让你的大脑更清醒、效率更高！

如果你需要，我可以：
1. 设定一个固定的提醒间隔（比如每 45 分钟提醒你一次）；
2. 根据你的作息定制专属喝水计划；
3. 分享一些有趣的小技巧帮你养成喝水习惯。

你想试试哪种方式呢？😊

```

## 示例6: 联网检索助手：AI如何上网获取信息

这个示例通过 requests 和 BeautifulSoup 库实现联网搜索和网页抓取。代码让 AI 判断是否需要联网，然后执行搜索或抓取。底层原理是 HTTP 请求和 HTML 解析，没有内置的网络能力，只是利用第三方库。

运行结果展示了天气查询功能。

```py
from sample.ai_utils import create_client, stream_chat_response, is_exit_command
import os
import requests
from bs4 import BeautifulSoup


client = create_client()


def search_web(query):
    """通用联网搜索（使用DuckDuckGo）"""
    try:
        # 使用DuckDuckGo的HTML搜索（无需API key）
        url = f"https://html.duckduckgo.com/html/?q={query}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        # 提取搜索结果
        results = []
        for result in soup.select('.result')[:5]:  # 取前5条
            title_elem = result.select_one('.result__a')
            snippet_elem = result.select_one('.result__snippet')

            if title_elem and snippet_elem:
                title = title_elem.get_text(strip=True)
                snippet = snippet_elem.get_text(strip=True)
                results.append(f"【{title}】\n{snippet}\n")

        if results:
            return "\n".join(results)
        else:
            return "未找到相关信息"

    except Exception as e:
        return f"搜索失败: {str(e)}"


def get_webpage_content(url):
    """获取网页内容"""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        # 移除脚本和样式
        for script in soup(["script", "style"]):
            script.decompose()

        # 获取文本内容
        text = soup.get_text()
        # 清理空白
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)

        # 限制长度
        if len(text) > 3000:
            text = text[:3000] + "..."

        return text
    except Exception as e:
        return f"获取失败: {str(e)}"


def ai_decide_action(msg):
    """让AI决定是否需要联网搜索"""
    prompt = f"""分析用户问题，判断是否需要联网搜索实时信息。

用户问题: {msg}

判断标准：
- 需要实时信息（天气、新闻、股票、机票、房价、最新事件等）：返回 "SEARCH: 搜索关键词"
- 需要访问特定网址：返回 "URL: 网址"
- 普通问答不需要联网：返回 "NORMAL"

只返回上述格式，不要有其他内容。"""

    completion = client.chat.completions.create(
        model="qwen3.5-plus",
        messages=[{"role": "user", "content": prompt}],
        extra_body={"enable_thinking": False},
        stream=False
    )

    return completion.choices[0].message.content.strip()


def ai_answer_with_context(question, search_results):
    """让AI结合搜索结果回答问题"""
    prompt = f"""基于以下搜索结果回答用户问题。

用户问题: {question}

搜索结果:
{search_results}

请基于搜索结果给出准确、简洁的回答。如果搜索结果中没有相关信息，请说明。"""

    completion = client.chat.completions.create(
        model="qwen3.5-plus",
        messages=[{"role": "user", "content": prompt}],
        extra_body={"enable_thinking": False},
        stream=True
    )

    return completion


print("=" * 60)
print("🤖 AI 助手已启动 (通用联网搜索)")
print("📝 功能:")
print("   - 自动判断是否需要联网")
print("   - 查询任何实时信息（新闻、机票、股票等）")
print("   - 访问任意网站")
print("💡 示例:")
print("   - 北京到上海机票价格")
print("   - 今天有什么重要新闻")
print("   - 特斯拉股价")
print("   - https://github.com 最新动态")
print("=" * 60)

while True:
    msg = input("\n你：").strip()

    if msg.lower() in ['exit', 'quit', '退出']:
        print("👋 再见！")
        break

    # 直接访问网址
    if msg.startswith('http://') or msg.startswith('https://'):
        print(f"\n🌐 正在访问 {msg}...")
        content = get_webpage_content(msg)
        print(f"\n📄 网页内容:\n{content[:1000]}")
        continue

    # 让AI决定如何处理
    print("🤔 AI 分析中...")
    action = ai_decide_action(msg)

    if action.startswith("SEARCH:"):
        # 需要联网搜索
        keyword = action.replace("SEARCH:", "").strip()
        print(f"🔍 正在搜索: {keyword}")

        search_results = search_web(keyword)

        if "未找到" in search_results or "失败" in search_results:
            print(f"\n{search_results}")
        else:
            print("\n" + "-" * 20 + "搜索结果" + "-" * 20)
            print(search_results)
            print("-" * 50)

            # 让AI基于搜索结果回答
            print("\n🤖 正在生成回答...")
            completion = ai_answer_with_context(msg, search_results)
            stream_chat_response(completion, title="AI回答")

    elif action.startswith("URL:"):
        # 访问指定网址
        url = action.replace("URL:", "").strip()
        print(f"🌐 正在访问 {url}...")
        content = get_webpage_content(url)
        print(f"\n📄 网页内容:\n{content[:1000]}")

    else:
        # 普通问答，不需要联网
        completion = client.chat.completions.create(
            model="qwen3.5-plus",
            messages=[{"role": "user", "content": msg}],
            extra_body={"enable_thinking": False},
            stream=True
        )
        stream_chat_response(completion, title="AI回答")

    print("\n" + "=" * 60)
```


运行结果：

```shell
============================================================
🤖 AI 助手已启动 (通用联网搜索)
📝 功能:
   - 自动判断是否需要联网
   - 查询任何实时信息（新闻、机票、股票等）
   - 访问任意网站
💡 示例:
   - 北京到上海机票价格
   - 今天有什么重要新闻
   - 特斯拉股价
   - https://github.com 最新动态
============================================================

你：深圳今天天气怎么样？
🤔 AI 分析中...
🔍 正在搜索: 深圳今天天气

--------------------搜索结果--------------------
【深圳天气预报,深圳7天天气预报,深圳15天天气预报,深圳天气查询】
深圳天气预报，及时准确发布中央气象台天气信息，便捷查询深圳今日天气，深圳周末天气，深圳一周天气预报，深圳蓝天预报，深圳天气预报，深圳40日天气预报，还提供深圳的生活指数、健康指数、交通指数、旅游指数，及时发布深圳气象预警信号、各类气象资讯。

【深圳市气象局（台）】
深圳天气 数据发布 城市天气 自动站查询 热 点 推 荐 2026年世界气象日 暗夜炼成生态宝藏星光化作经济动能 深圳气象推动西涌暗夜社区打造成"两山"转化国际示范标杆 10年如一暖心护航 深圳气象春运探路团今日启程北上 全运会气象服务专题 2025年深圳"气象 ...

【【深圳天气预报】深圳天气预报一周,深圳天气预报15天,30天,今天,明天,7天,10天,未来深圳一周天气预报查询—天气网】
天气网提供深圳天气预报15天,30天,今日天气,明天天气,深圳未来一周的天气预报,广东深圳天气,深圳实时天气查询,深圳天气预报一周,7天,10天,40天的天气情况。旅游出行,从天气网开始!

【【深圳市天气】_深圳市天气预报_天气查询 - 墨迹天气】
深圳市今天实况：25度 晴，湿度：70%，东南风：3级。白天：29度,多云。 夜间：多云，22度，天气较热，墨迹天气建议您选择短袖上衣加七分裤的搭配，针织衫是进出空调房的必备单品。

【【深圳24小时天气查询】_深圳今日逐小时天气预报查询_2345天气预报】
2345天气预报为您提供深圳24小时天气详情、深圳今日天气预报，包括实时温度、风力风向、空气质量、湿度、气压、降水概率、紫外线强度等，每小时更新一次!

--------------------------------------------------

🤖 正在生成回答...

--------------------AI回答--------------------
根据搜索结果，深圳今天的天气情况如下：

*   **当前实况**：气温 25℃，晴朗，湿度 70%，东南风 3 级。
*   **白天预报**：多云，最高气温 29℃。
*   **夜间预报**：多云，最低气温 22℃。
*   **穿衣建议**：天气较热，建议穿着短袖上衣加七分裤；进出空调房可备一件针织衫。

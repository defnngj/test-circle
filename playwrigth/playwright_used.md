## playwright 辅助工具

playwright 作为微软新出的自动化工具，公众号已经写过几篇文章来介绍了。本文介绍一下他提供的辅助工具的用法。虽然，官网上有介绍，但是你不一定能看懂，反正，我是摸索了好半天。


__准备工作__

以python为例，先通过`pip` 安装相关库。

```shell
> pip instalal pytest==6.2.5
> pip install playwright==1.20.0
> pip install pytest-playwright==0.3.0
```

### Inspector

playwright Inspector 是一个GUI工具，可以帮助创作和调试剧作家脚本。

1. 首先，创建一个目录和文件。

test_dir/
└── test_sample.py


`test_sample.py` 脚本内容：

```py
from playwright.sync_api import Page


def test_example_is_working(page: Page):
    page.goto("https://example.com")
    assert page.inner_text('h1') == 'Example Domain'
    page.click("text=More information")

```

2. 启动 Inspector。


```shell
> cd test_dir
> $env:PWDEBUG=1
> pytest -s
```

注意：

1. 必须在 `test_dir` 目录下面，防止 pytest 发现别的用例去执行了。
2. `$env:PWDEBUG=1` 用于设置环境变量，这里以在`PowerShell` 下面为例。
3. `pytest -s` 会检索当前目录下面的测试用例，`test_sample.py` 必须符合pytest规则。

只有做对了上面三步才能看到 Inspector。


## Trace Viewer

playwright Trace Viewer 是一个GUI工具，可以帮助探索脚本运行后记录的剧作家跟踪。在本地或浏览器中打开trace.playwright.dev。

```py
# test_trace.py
from playwright.sync_api import sync_playwright



with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()

    # Start tracing before creating / navigating a page.
    context.tracing.start(screenshots=True, snapshots=True, sources=True)

    page = context.new_page()
    page.goto("https://www.baidu.com/")
    page.fill('input[name="wd"]', "playwright")
    page.click('input[type="submit"]')

    # Stop tracing and export it into a zip archive.
    context.tracing.stop(path="trace.zip")
```

官方的例子不全，注意看`page` 的赋值：

*  `page = context.new_page()` 正确。
 
*  `page = browser.new_page()` 错误。


__执行脚本__

```
> python test_trace.py
```

__本地打开__

你会在脚本的所在目录得到一个 `trace.zip` 文件。本地打开：

```
> playwright show-trace trace.zip
```

__网站打开__

访问：https://trace.playwright.dev/


上面有个上传文件的按钮，将 `trace.zip` 文件上传。


### Test Generator

playwright 能够生成现成的测试，


这个功能相对前两个坑就简单很多了。直接终端执行命令：

```shell
> playwright codegen www.baidu.com
```


在操作的过程录制脚本。


## 总结

以上三个算是 playwright 的辅助工具，不管是 Inspector 还是 Trace 都可以很好的辅助我们编写和分析测试用例。但是，官方的文档写得真让人迷惑。


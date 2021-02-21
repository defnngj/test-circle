# 自动化测试工具palywright

## 前言

我们介绍许多e2e的自动化测试工具

一类是基于 Selenium 的测试框架：

* robot framework
* gauge
* SeleniumBase
* seldom（虫师维护的）

另一类是基于JS语言的测试工具：

* cypress
* puppeteer

前都本身就是基于Selenium的自动化测试工具，后者在测试人员这个圈子也是未能撼动Selenium的地位，我认为有两个原因，一是Selenium是一个非常成熟的自动化测试工具，有大量的学习资料；另一方面selenium支持Python，没错Python以其简单的语法已经成为了测试人员学习编程语言的不二之选。

好了，介绍个新的自动化测试工具还要铺垫这么多？这是因为我看了palywright的文档之后，觉得这工具大概率能在测试人员这个群体中流行起来。


## playwright 介绍

官方：https://playwright.dev/

__介绍__

> Playwright enables fast, reliable and capable automation across all modern browsers.

__支持平台&浏览器__

|          | Linux | macOS | Windows |
|   :---   | :---: | :---: | :---:   |
| Chromium <!-- GEN:chromium-version -->89.0.4344.0<!-- GEN:stop --> | ✅ | ✅ | ✅ |
| WebKit <!-- GEN:webkit-version -->14.1<!-- GEN:stop --> | ✅ | ✅ | ✅ |
| Firefox <!-- GEN:firefox-version -->84.0b9<!-- GEN:stop --> | ✅ | ✅ | ✅ |

__支持语言__

* JavaScript and TypeScript: https://github.com/microsoft/playwright
* Java: https://github.com/microsoft/playwright-java
* Python: https://github.com/microsoft/playwright-python
* C#: https://github.com/microsoft/playwright-sharp

从支持的平台、语言和浏览器来看，是不是有Selenium的味道。这是微软爸爸的项目，从微软这几年拥抱开源的态度来看，这个工具应该会得到持续的支持。

## 安装

不同的语言安装方式不同，根据上面的链接，到对应的项目下面查看安装方式。本文以Python为例。

安装plywright

```shell
> pip install playwright
```

安装浏览器

```shell
> python -m playwright install

Downloading chromium v827102 - 89.4 Mb [====================] 100% 0.0s
chromium v827102 downloaded to C:\Users\fnngj\AppData\Local\ms-playwright\chromium-827102
Downloading firefox v1205 - 74.9 Mb [====================] 100% 0.0s
firefox v1205 downloaded to C:\Users\fnngj\AppData\Local\ms-playwright\firefox-1205
Downloading webkit v1383 - 51.4 Mb [====================] 100% 0.0s
webkit v1383 downloaded to C:\Users\fnngj\AppData\Local\ms-playwright\webkit-1383
```

## 录制脚本

plywright可以在浏览器中记录用户的互动并生成代码。

执行命令
```
> python -m playwright codegen
```

视频

接下来，对录制的脚本做简单的修饰。

```shell
from time import sleep
from playwright import sync_playwright


def run(playwright):
    pw = playwright().start()
    browser = pw.chromium.launch(headless=False)
    context = browser.newContext()

    # Open new page
    page = context.newPage()

    # Go to https://www.baidu.com/
    page.goto("https://www.baidu.com/")

    # Fill input[name="wd"]
    page.fill('input[name="wd"]', "playwright")

    # Click input[type="submit"]
    page.click('input[type="submit"]')

    sleep(2)

    # assert title
    assert page.title() == "playwright_百度搜索"
    # ---------------------
    context.close()
    browser.close()


if __name__ == '__main__':
    run(sync_playwright)
```

从API来看，和大多数自动化工具都差不多。


## 异步的写法

playwright官方例子中给出的异步的写法。 从它提供的API `sync_playwright` 的命名也可以看出，它很喜欢异步。

```python
import asyncio
from playwright import async_playwright


async def main():
    async with async_playwright() as p:
        for browser_type in [p.chromium, p.firefox, p.webkit]:
            browser = await browser_type.launch(headless=False)
            page = await browser.newPage()
            await page.goto('https://www.baidu.com')
            await page.screenshot(path=f'example-{browser_type.name}.png')
            await browser.close()

asyncio.get_event_loop().run_until_complete(main())
```

后续：
1. playwrigth 与其他自动化工具的比较
2. playwright API介绍
3. playwright 与单元测试框架unittest/pytest的使用

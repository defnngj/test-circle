## playwright基于python安装


## playwright 支持多种语言：

node.js: https://github.com/microsoft/playwright  41.5K star
python: https://github.com/microsoft/playwright-python  6.8K star
.net: https://github.com/microsoft/playwright-dotnet  1.6k star
java: https://github.com/microsoft/playwright-java  533 star


## 安装

- [x] python

* 下载地址

https://www.python.org/downloads/

> 根据自己的平台选择 python 3.7+ 版本即可。


* 查看版本

```shell
> python --version
Python 3.8.6

> pip show pip
Version: 22.2.2
```

- [x] playwright

* 安装playwright

```
> pip install playwright
```

* 安装浏览器&驱动

```
> playwright install
```


## 编写测试用例


* 同步测试例子

```python
# playwright_sync.py
from playwright.sync_api import sync_playwright
from playwright.sync_api import expect


with sync_playwright() as p:
    # 启动浏浏览器
    browser = p.chromium.launch()
    # 创建新的页面
    page = browser.new_page()
    # 进入指定URL
    page.goto("http://playwright.dev")
    print(page.title())
    # 断言标题
    expect(page).to_have_title("Fast and reliable end-to-end testing for modern web apps | Playwright")

    # 获得元素
    get_started = page.locator('text=Get Started')
    # 断言元素属性
    expect(get_started).to_have_attribute('href', '/docs/intro')
    # 元素执行点击
    get_started.click()

    # 断言URL
    expect(page).to_have_url('https://playwright.dev/docs/intro')

    # 关闭浏览器
    browser.close()

```

* 异步测试例子


```python
# playwright_async.py
import asyncio
from playwright.async_api import async_playwright


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto("http://playwright.dev")
        print(await page.title())
        await browser.close()

asyncio.run(main())

```

## 运行测试

进入项目`py_project\`目录，通过下面的命令运行测试。

* 运行命令

```shell
> python playwright_sync.py

Fast and reliable end-to-end testing for modern web apps | Playwright
```



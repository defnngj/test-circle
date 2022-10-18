## playwrgit 常用 API

这里将 playwright的一些API 做个简单的汇总和介绍。

* 启动浏览器

```python
from playwright.sync_api import sync_playwright

p =  sync_playwright().start()

# 启动浏浏览器
# "msedge", "chrome-beta", "msedge-beta", "msedge-dev"
browser = p.chromium.launch(channel="chrome")
browser = p.firefox.launch()
browser = p.webkit.launch()

# 创建新的页面
page = browser.new_page()

# 关闭浏览器
browser.close()
```

* 上下文

```python
 # 上下文页面
context = browser.new_context()

page = context.new_page()

context.close()
```

* 浏览器操作

```python
page.goto("https://playwright.dev")
page.reload()
page.go_back()
page.go_forward()
```

* 执行js

```python
href = page.evaluate('() => document.location.href')
```


* 表单

```python
# Locate element inside frame
# Get frame using any other selector
username = page.frame_locator('.frame-class').locator('#username-input')
username.fill('John')
```


* 输入

https://playwright.dev/python/docs/input

* 包含API
  * Text input
  * Checkboxes and radio buttons
  * Select options
  * Mouse click
  * Type characters
  * Keys and shortcuts
  * Upload files
  * Focus element


* 截图

```python
page.screenshot(path="screenshot.png")
```

* 警告框

```python
page.on("dialog", lambda dialog: dialog.accept())
page.on("dialog", lambda dialog: print(dialog.message))
```


* 下载

```python
with page.expect_download() as download_info:
    page.locator("a").click()
download = download_info.value
# wait for download to complete
path = download.path()
```

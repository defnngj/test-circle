# playwright 断言

断言一般是单元测试框架所提供的概念，一般`相等`、`包含`、`布尔(True/False)` 等。

playwright为您提供了Web-First断言，以及创建断言的方便方法，这些断言将等待并重试，直到满足预期的条件。

* 例子

```py
from playwright.sync_api import Page, expect

def test_status_becomes_submitted(page: Page) -> None:
    # ..
    page.locator("#submit-button").click()
    expect(page.locator(".status")).to_have_text("Submitted")
```

官方文档：
https://playwright.dev/python/docs/test-assertions



```python
import re
from playwright.sync_api import expect

# 断言标题
expect(page).to_have_title(re.compile(r".*checkout"))

# 断言URL
expect(page).to_have_url(re.compile(".*checkout"))

# 断言文本
locator = page.locator(".title")
expect(locator).to_have_text(re.compile(r"Welcome, Test User"))

# 断言属性
locator = page.locator("input")
expect(locator).to_have_attribute("type", "text")

# 断言class属性
locator = page.locator("#component")
expect(locator).to_have_class(re.compile(r"selected"))

# 断言元素数量
locator = page.locator("list > .component")
expect(locator).to_have_count(3)

```
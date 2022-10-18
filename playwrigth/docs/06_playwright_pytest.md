# 基于pytest使用playwright

playwright提供了`playwright-pytest` 项目，更好的将playwright和 pytest单元测试框架做了整合。

https://github.com/microsoft/playwright-pytest


## 安装playwright-pytest

```
> pip install pytest
> pip install pytest-playwright
```

## playwright-pytest使用


### pytest基本用法1

```python
# test_pytest_demo1.py
# 被测函数
def inc(x):
    return x + 1


# 测试用例
def test_answer():
    assert inc(3) == 5

```

* 运行测试

```shell
pytest .\test_pytest_demo1.py
=================== test session starts ==================================

test_pytest_demo1.py .                                    [100%]

==================== 1 passed in 0.05s ===================================
```



### pytest基本用法2

```python
# test_pytest_demo2.py
import pytest


# 被测函数
def inc(x):
    return x + 1


# 测试用例
def test_answer():
    assert inc(3) == 4


if __name__ == '__main__':
    pytest.main(["test_pytest_demo2.py"])

```

* 运行测试

```shell
> python .\test_pytest_demo2.py
=================== test session starts ==================================

test_pytest_demo1.py .                                    [100%]

==================== 1 passed in 0.05s ===================================
```

## playwright-pytest

参考官方文档：https://playwright.dev/python/docs/intro

```python
# test_sample.py
import re
from playwright.sync_api import Page, expect


def test_playwright_page(page: Page):
    page.goto("https://playwright.dev/")

    # Expect a title "to contain" a substring.
    expect(page).to_have_title(re.compile("Playwright"))

    # create a locator
    get_started = page.locator("text=Get Started")

    # Expect an attribute "to be strictly equal" to the value.
    expect(get_started).to_have_attribute("href", "/docs/intro")

    # Click the get started link.
    get_started.click()

    # Expects the URL to contain intro.
    expect(page).to_have_url(re.compile(".*intro"))


```

* 运行测试

```shell
> pytest .\test_sample.py
> pytest --browser firefox .\test_sample.py
```



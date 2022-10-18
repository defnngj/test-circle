# 基于unittest使用playwright

在python语言中，playwright上是一个测试库，他并不包含测试用例、测试报告等单元测试框架的东西，需要和单元测试框架结合去完成自动化测试项目。可以选择`unittest`、`pytest` 等。

https://playwright.dev/python/docs/library

## unittest

unittest是集成到Python中的标准库，先来看以下他的基本用法。

* 编写例子

```python
# unittest_demo.py
import unittest


class Playwright(unittest.TestCase):

    def setUp(self):
        print("start test")

    def tearDown(self):
        print("end test")

    def test_start(self):
        self.assertEqual(2+2, 4)


if __name__ == '__main__':
    unittest.main()

```

* 运行测试

```shell
> python .\unittest_demo.py
start test
end test
.
----------------------------------------------------------------------
Ran 1 test in 0.000s

OK
```

## playwright + unittest

将playwright的API填充到unittest框架中。


```python
# playwright_unittest.py
import unittest
from playwright.sync_api import sync_playwright
from playwright.sync_api import expect


class Playwright(unittest.TestCase):

    def setUp(self):
        p = sync_playwright().start()
        self.browser = p.chromium.launch()
        self.page = self.browser.new_page()

    def tearDown(self):
        self.browser.close()

    def test_start(self):
        page = self.page
        page.goto("http://playwright.dev")
        print(page.title())
        expect(page).to_have_title("Fast and reliable end-to-end testing for modern web apps | Playwright")

        get_started = page.locator('text=Get Started')
        expect(get_started).to_have_attribute('href', '/docs/intro')
        get_started.click()

        expect(page).to_have_url('https://playwright.dev/docs/intro')


if __name__ == '__main__':
    unittest.main()
```

* 运行测试

```
> python playwright_unittest.py
```


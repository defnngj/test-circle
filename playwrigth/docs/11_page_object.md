# page object模式


可以对大型测试套件进行结构化，以优化编写和维护的便利性。Page Object Models就是这样一种构建测试套件的方法。

优点：

* page object简化了编写。它们创建适合您的应用程序的高级API。
* page object模式化了维护。它们在一个地方捕获元素选择器，并创建可重用代码以避免重复。


* 定义page

```python
# models/search.py
class SearchPage:
    def __init__(self, page):
        self.page = page
        self.search_term_input = page.locator('[aria-label="Enter your search term"]')

    def navigate(self):
        self.page.goto("https://bing.com")

    def search(self, text):
        self.search_term_input.fill(text)
        self.search_term_input.press("Enter")
```

* 定义用例

```python
# test_search.py
from models.search import SearchPage

# in the test
page = browser.new_page()
search_page = SearchPage(page)
search_page.navigate()
search_page.search("search query")
```

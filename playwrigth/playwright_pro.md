# playwright自动化项目搭建

这是关于playwright系列介绍的最后一篇。搭建基于 playwright 的自动化项目。

GitHub地址: https://github.com/defnngj/playwright-pro

## 具备功能

关键技术：

* pylaywright测试库
* pytest单元测试框架
* pytest-playwright插件

非关键技术：

* pytest-html插件
* pytest-rerunfailures插件
* seldom 测试框架

实现功能：

* 元素定位与操作分离
* 失败自动截图并保存到HTML报告
* 失败重跑
* 可配置不同的浏览器执行
* 可配置`headless/headful` 模式
* 实现参数化读取数据文件

一个自动化具备的基本功能差不多就这些了。其实主要是使用了一堆框架和插件，主要是整合能力。


## 使用方式

* 安装依赖

```shell
$ pip install -r requirements.txt
```

注：安装```requirements.txt```指定依赖库的版本，这是经过测试的，有时候新的版本可会有错。

* 配置

在 `config.py` 文件配置

```python
class RunConfig:
    """
    运行测试配置
    """
    # 运行测试用例的目录或文件
    cases_path = "./test_dir/test_parametrize.py"

    # 配置浏览器驱动类型(chromium, firefox, webkit)。
    browser = "chromium"

    # 运行模式（headless, headful）
    mode = "headful"

    # 配置运行的 URL
    url = "https://www.baidu.com"

    # 失败重跑次数
    rerun = "0"

    # 当达到最大失败数，停止执行
    max_fail = "5"
```

* 运行

运行测试

```shell
$ python run.py
```

## 设计细节

* 关于page object设计模式

page object是自动化测试最常用的设计模式。

但 playwright 中的只提供了操作方法，`元素定位`和`测试数据`都只是参数。

```python
# 输入
page.type('#kw', "playwright")
# 点击
page.click('#su')
```

我们依然，可以将元素定位单独封装一层。

```py
class BaiduElem:
    search_input = "#kw"  # 搜索框
    search_button = "#su"  # 搜索按钮
    settings = "#s-usersetting-top"  # 设置
    search_setting = "#s-user-setting-menu > div > a.setpref"  # 搜索设置
    save_setting = 'text="保存设置"'  # 保存设置
```

在测试用例中的使用
```py
from element.baidu_element import BaiduElem
from playwright.sync_api import Page


def test_baidu_search(page: Page, base_url):
    """
    """
    page.goto(base_url)
    page.type(BaiduElem.search_input, text="playwright")
    page.click(BaiduElem.search_button)
    sleep(2)
    assert page.title() == "playwright_百度搜索"
```

这肯定不是什么好的设计。用例层写起来会比较啰嗦， 最好可以`page.elem.type("playwright")` 的语法实现，这就需要在playwright的基础上再封装一套API, 看playwright 源码还是有些复杂的，主要是用了很多就异步，成本比较大，暂时先这么用。


* 关于自动截图

自动截图需要 pytest/pytest-html  和  playwright 配合完成， pytest/pytest-html 判断用例实现，并把图片插入到报告中。 playwright 实现截图动作。

```python
@pytest.mark.hookwrapper
def pytest_runtest_makereport(item):
    """
    用于向测试用例中添加用例的开始时间、内部注释，和失败截图等.
    :param item:
    """
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    report.description = description_html(item.function.__doc__)
    extra = getattr(report, 'extra', [])
    page = item.funcargs["page"]
    if report.when == 'call':
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            case_path = report.nodeid.replace("::", "_") + ".png"
            if "[" in case_path:
                case_name = case_path.split("-")[0] + "].png"
            else:
                case_name = case_path

            capture_screenshots(case_name, page)
            img_path = "image/" + case_name.split("/")[-1]
            if img_path:
                html = '<div><img src="%s" alt="screenshot" style="width:304px;height:228px;" ' \
                       'onclick="window.open(this.src)" align="right"/></div>' % img_path
                extra.append(pytest_html.extras.html(html))
        report.extra = extra

def capture_screenshots(case_name, page):
    """
    配置用例失败截图路径
    :param case_name: 用例名
    :return:
    """
    global driver
    file_name = case_name.split("/")[-1]
    if RunConfig.NEW_REPORT is None:
        raise NameError('没有初始化测试报告目录')
    else:
        image_dir = os.path.join(RunConfig.NEW_REPORT, "image", file_name)
        page.screenshot(path=image_dir)
```

通过`page = item.funcargs["page"]` 拿到playwright的驱动，截图判断逻辑有点复杂，不过我已经实现了。

## 总结

* playwright还不稳定，我在使用的时候时常报一些错误，错误日志也不友好。计划在正式项目中使用的谨慎考虑，估计有一些坑要踩。
* 不熟悉playwright的API，可以通过官方文档，或者是项目自带的测试用例，或者阅读项目源码都是很好的学习方式。

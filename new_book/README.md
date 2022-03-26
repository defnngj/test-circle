# 自动化测试框架设计

* [背景](./00_idea.md)

* 自动化测试框架设计基础
  * [相关概念](./01_test_framework.md)
  * [框架设计基础](./02_test_framework.md)

* 单元测试框架
  * [单元测试框架介](./03_unittest_framework.md)
  * [基于unittest扩展](./05_unittest_extend.md)
  * [基于pytest实现插件](./04_pytest_plug_in.md)
  * [构建python包](./06_setup_.md)

* Web UI测试
  * 主流测试库介绍
  * Selenium API 封装
  * [方法链（Method Chaining）](./07_method_chaining.md)
  * 自动管理浏览器驱动
  * 元素智能等待
  * 元素高亮显示
  * 设计断言

* app UI测试
  * 主流移动测试库
  * appium API 封装
  * uiautomator2 API 集成

* HTTP测试
  * 主流HTTP测试库
  * requests API 封装
  * 设计断言
  * 数据库操作

* Page object设计模式
  * page object设计模式
  * 自定义Page object设计模式
  * webium库设计原理
  * poium库设计原理

* 测试报告
  * HTML测试报告
  * XML测试报告
  * JSON测试报告

* 数据驱动
  * 数据驱动库
  * 支持多种数据文件

* 异常与日志
  * 自定义异常类
  * 引入日志库
  * 字符画

* 实现命令行工具
  * 命令行工具介绍
  * 生成命令行命令
  * 设计脚手架

* 其他扩展开发
  * 集成封装自动发邮件
  * 生成测试数据数据
  * 实现用例依赖

* 发布框架到pypi仓库


### 扩展库

* 单元测试框架
  * [unittest](https://docs.python.org/zh-cn/3/library/unittest.html)
  * [pytest](https://github.com/pytest-dev)
  * [QTAF](https://github.com/Tencent/QTAF)

* Web UI测试
  * [playwright](https://github.com/microsoft/playwright-python)
  * [selenium](https://github.com/SeleniumHQ/selenium)
  * [puppeteer](https://github.com/puppeteer/puppeteer)

* app UI测试
  * [appium](https://github.com/appium/appium)
  * [airtest](https://github.com/AirtestProject/Airtest)
  * [openatx](https://github.com/openatx/uiautomator2)

* HTTP测试
  * [requests](https://github.com/psf/requests)
  * [httpx](https://github.com/encode/httpx)
  * [aiohttp](https://github.com/aio-libs/aiohttp)
  * [jsonschema](https://github.com/Julian/jsonschema)
  * [jmespath](https://github.com/jmespath/jmespath.py)

* Page object设计模式
  * [webium](https://github.com/wgnet/webium)
  * [poium](https://github.com/SeldomQA/poium)

* 测试报告
  * [HTMLTestRunner](https://github.com/SeldomQA/HTMLTestRunner)
  * [unittest-xml-reporting](https://github.com/xmlrunner/unittest-xml-reporting)
  * [xmltodict](https://github.com/martinblech/xmltodict)

* 数据驱动
  * [parameterized](https://github.com/wolever/parameterized)
  * [ddt](https://github.com/datadriventests/ddt)

* 异常与日志
  * [colorama](https://github.com/tartley/colorama)
  * [loguru](https://github.com/Delgan/loguru)

* 实现命令行工具
  * [click](https://github.com/pallets/click)
  * [python-fire](https://github.com/google/python-fire)
  * [typer](https://github.com/tiangolo/typer)

* 其他扩展开发
  * [yagmail](https://github.com/kootenpv/yagmail)
  * [faker](https://github.com/joke2k/faker)


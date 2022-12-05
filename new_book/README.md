# 自动化测试框架设计

* [背景](./00_idea.md)

* 自动化测试框架设计基础
  * [相关概念](./01_test_framework.md)
  * [框架设计基础](./02_test_framework.md)
  * [构建python包](./06_setup_.md)

* 单元测试框架
  * [单元测试框架介](./03_unittest_framework.md)
  * [基于unittest扩展](./05_unittest_extend.md)
  * [基于pytest实现插件](./04_pytest_plug_in.md)

* 测试报告设计
  * [基于unittest重写测试报告](./11_test_report.md)
  * [如何获取HTML模板](./12_html_template.md)
  * [Jinja模板引擎](./13_jinja2_template.md)
  * [unittest生成HTML测试报告](./14_test_report_html.md)

* 自动发送服务
  * 发送邮件
  * 发送钉钉
  * 发送企业微信
  * 发送飞书

* 数据驱动设计
  * [unittest数据驱动扩展](./15_data_driver.md)
  * [实现 @data 装饰器](./16_data_driver.md)
  * [基于 @data 支持dict格式](./16_data_driver.md)
  * [实现 @file_data 装饰器](./17_data_driver.md)


* 数据库操作封装
  * [数据库操作技术](./18_db_operation.md)
  * [数据库操作封装](./19_db_dev.md)

* 随机数据自动生成
  * [随机数测试库介绍](./20_testdata_lib.md)
  * [设计常用测试数据](./21_testdata_dev.md)

* 实现命令行工具
  * 命令行工具介绍
  * 生成命令行命令
  * 设计脚手架

* 其他设计
  * 用例依赖
  * 分类标签
  * 打印日志
  * 自定义异常类型
  * 缓存cache

* Web UI测试
  * 主流测试库介绍
  * [Selenium API 封装](./07_selenium_api_dev.md)
  * [方法链（Method Chaining）](./08_method_chaining.md)
  * [自动管理浏览器驱动](./09_browser_driver.md)
  * 元素智能等待
  * 元素高亮显示
  * 设计UI元素断言

* app UI测试
  * 主流移动测试库
  * appium API 封装
  * uiautomator2 API 集成

* HTTP测试
  * 主流HTTP测试库
  * requests API 封装
  * 设计接口断言
  * 数据库操作

* Page object设计模式
  * page object设计模式
  * 自定义Page object设计模式
  * webium库设计原理
  * poium库设计原理

* 平台化支持
  * 提取自动化用例信息
  * 执行自动化用例
  * 接入平台
  * 平台化执行&报告

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
  * [pywebreport](https://github.com/yongchin0821/pywebreport)
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

* 数据库
  * [pymysql](https://github.com/PyMySQL/PyMySQL)
  * [pymssql](https://github.com/pymssql/pymssql)
  * [sqlalchemy](https://github.com/sqlalchemy/sqlalchemy)
  * [dbpy](https://github.com/whiteclover/dbpy)
  * [tinydb](https://github.com/msiemens/tinydb)

* 随机数据
  * [testdata](https://github.com/Jaymon/testdata)
  * [faker](https://github.com/joke2k/faker)
  * [hypothesis](https://github.com/HypothesisWorks/hypothesis)

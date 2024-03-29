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
  * [命令行工具介绍](./27_command.md)
  * [实现脚手架](./28_command_used.md)
  * [实现性能工具](./28_command_used.md)
  * [生成命令行工具](./28_command_used.md)

* 其他设计
  * [用例依赖](./22_case_depend.md)
  * [用例分类标签](./23_case_labels.md)
  * [打印日志](./25_logger.md)
  * [自定义异常](./26_logger.md)
  * [缓存cache](./24_cache.md)

* Web UI测试
  * [主流测试库介绍](./29_web_testing_framework.md)
  * [Selenium API 封装](./07_selenium_api_dev.md)
  * [方法链（Method Chaining）](./08_method_chaining.md)
  * [自动管理浏览器驱动](./09_browser_driver.md)
  * [设计Web测试断言](./30_web_testing_assert.md)

* app UI测试
  * [App移动测试工具](./35_app_testing.md)
  * [appium 基本使用](./36_app_testing.md)
  * [appium API 封装](./37_appium_api.md)

* HTTP测试
  * [主流HTTP测试库](./31_http_testing.md)
  * [封装 HTTP 测试库 API](./32_http_api.md)
  * [设计接口测试断言](./33_http_assert.md)
  * [装接口检查装饰器](./34_decorator.md)

* Page object设计模式
  * [设计模式和开发策略](./38_po_base.md)
  * [page object测试库](./39_po_lib.md)
  * [poium库设计原理](./40_poium_core.md)

* 平台化支持
  * [测试平台介绍](./41_test_platform.md)
  * [unittest平台化支持](./42_code_platform.md)
  * [seldom-platform](./43_seldom_platform.md)

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
  * [logzero](https://github.com/metachris/logzero)

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

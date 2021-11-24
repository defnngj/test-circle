# 自动化测试框架设计

1. 自动化测试框架设计基础
  1.1. 本书定位
  1.2. 框架与项目

2. 单元测试框架
  2.1. 单元测试框架介
  2.2. 基于unittest扩展
  2.3. 基于pytest实现插件
  3.4. 设计`setup.py`安装文件

3. Web UI测试
  3.1. 主流测试库介绍
  3.2. Selenium API 封装
  3.2. 自动管理浏览器驱动
  3.3. 元素智能等待
  3.4. 元素高亮显示
  3.5. 设计断言

4. app UI测试
  4.1. 主流移动测试库
  4.2. appium API 封装
  4.3. uiautomator2 API 集成

5. HTTP测试
  5.1. 主流HTTP测试库
  5.2. requests API 封装
  5.3. 设计断言
  5.4. 数据库操作

6. Page object设计模式
  5.1 page object设计模式
  5.2 自定义Page object设计模式
  5.3 webium库设计原理
  5.4. poium库设计原理

7. 测试报告
  7.1 HTML测试报告
  7.2 XML测试报告
  7.3 JSON测试报告

8. 数据驱动
  8.1 数据驱动库
  8.2 基于parameterized二次开发

9. 异常与日志
  9.1 自定义异常类
  9.2 引入日志库
  9.3 字符画

10. 实现命令行工具
  10.1 命令行工具介绍
  10.2 生成命令行命令
  10.3 设计脚手架

11. 其他扩展开发
  11.1 集成封装自动发邮件
  11.2 生成测试数据数据
  11.3 实现用例依赖

12. 发布框架到pypi仓库


### 扩展库

2. 单元测试框架
   * [unittest](https://docs.python.org/zh-cn/3/library/unittest.html)
   * [pytest](https://github.com/pytest-dev)
   * [QTAF](https://github.com/Tencent/QTAF)

3. Web UI测试
   * [playwright](https://github.com/microsoft/playwright-python)
   * [selenium](https://github.com/SeleniumHQ/selenium)
   * [puppeteer](https://github.com/puppeteer/puppeteer)

4. app UI测试
   * [appium](https://github.com/appium/appium)
   * [airtest](https://github.com/AirtestProject/Airtest)
   * [openatx](https://github.com/openatx/uiautomator2)

5. HTTP测试
   * [requests](https://github.com/psf/requests)
   * [httpx](https://github.com/encode/httpx)
   * [aiohttp](https://github.com/aio-libs/aiohttp)
   * [jsonschema](https://github.com/Julian/jsonschema)
   * [jmespath](https://github.com/jmespath/jmespath.py)

6. Page object设计模式
   * [webium](https://github.com/wgnet/webium)
   * [poium](https://github.com/SeldomQA/poium)

7. 测试报告
   * [HTMLTestRunner](https://github.com/SeldomQA/HTMLTestRunner)
   * [unittest-xml-reporting](https://github.com/xmlrunner/unittest-xml-reporting)
   * [xmltodict](https://github.com/martinblech/xmltodict)

8. 数据驱动
   * [parameterized](https://github.com/wolever/parameterized)
   * [ddt](https://github.com/datadriventests/ddt)

9. 异常与日志
   * [colorama](https://github.com/tartley/colorama)
   * [loguru](https://github.com/Delgan/loguru)

10. 实现命令行工具
   * [click](https://github.com/pallets/click)
   * [python-fire](https://github.com/google/python-fire)
   * [typer](https://github.com/tiangolo/typer)

11. 其他扩展开发
   * [yagmail](https://github.com/kootenpv/yagmail)
   * [faker](https://github.com/joke2k/faker)


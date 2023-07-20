## Pylenium: 让Python Web测试变得更简单


关于 selenium 的二次开发项目层出不穷，作为一个Selenium老用户，会时长关注一些优秀的二次开发项目，借鉴他们优秀的设计。当然，这些项目一般分以下几类。

* 单纯针对 Selenium 的API做二次封装，提供更简洁的 API。例如 helium。

* 把 selenium 和 另外一个工具进行缝合，提供更多的功能。例如 selenium-requests。

* 把 selenium 和 测试框架进行整合，以便提供更好的 自动化测试体验，例如 seleniumbase、seldom 等。 

* 把 selenium 封装成 关键字，提供 特定领域语言，例如 robotframework-seleniumLibrary。

....

这充分说明了 selenium 应用广泛，可塑性极强！哈哈。


### Pylenium 介绍


官方文档：https://docs.pylenium.io/


__简述__

> Bring the best of Selenium, Cypress and Python into one package.

看作者的描述，是想把 selenium 变得像  Cypress !? 🤔 


__特色__

* Automatic waiting and synchronization

* Quick setup to start writing tests

* Easy to use and clean syntax for amazing readability and maintainability

* Automatic driver installation so you don't need to manage drivers

* Leverage the awesome Python language

* and more!


从特性来看，`智能等待` 和 `自动安装驱动` 算是亮点，其他都是废话。


__安装__

* pip 安装

```bash
pip install pyleniumio

---or---

pipenv install pyleniumio

---or---

poetry add pyleniumio
```

###   Pylenium 使用


__初始化__

准备好一个目录，初始化项目。

```bash
pylenium init
```

这类似于脚手架，会自动生成三个文件。


* `conftest.py` - 它包含Pylenium所需的fixture。`conftest.py` 是 pytest 的测试配置文件，里面实现了一些钩子函数和扩展。项目的核心就在这个文件里了。

例如：针对 Faker 提供一个 fake 钩子函数。在用例里面可以使用 fake 来生成一些随机数。

```py
import pytest
from faker import Faker

@pytest.fixture(scope="function")
def fake() -> Faker:
    """A basic instance of Faker to make test data."""
    return Faker()

```

* `pylenium.json` - 这是Pylenium的配置文件。把自动化测试的配置以为 JSON 的方式提供。

例如： 浏览器名称，等待时间等。

```json
{
  "driver": {
    "browser": "chrome",
    "remote_url": "",
    "wait_time": 10,
    "page_load_wait_time": 0,
    "options": [],
    "capabilities": {},
    "version": null,
    "experimental_options": null,
    "extension_paths": [],
    "webdriver_kwargs": {},
    "seleniumwire_enabled": false,
    "seleniumwire_options": {},
    "local_path": ""
  },
  "logging": {
    "screenshots_on": true
  },
  "viewport": {
    "maximize": true,
    "width": 1440,
    "height": 900,
    "orientation": "portrait"
  },

  "customer": {}
}
```

`pytest.ini` - 这是pytest的配置文件。

例如：配置日志的格式、级别等。

```ini
[pytest]
; Configuring pytest
; More info: https://docs.pytest.org/en/6.2.x/customize.html

;Logging
; DATE FORMAT EXAMPLE: %Y-%m-%d %H:%M:%S
log_cli_format = %(asctime)s %(levelname)-8s %(name)-8s %(message)s
log_cli_level = COMMAND
log_cli_date_format = %H:%M:%S
```

__使用例子__

当然，复杂的事情都让 上面的三个的文件干了，用例编写起来自然就简单了许多。

```py
# pylenium

def test_google_search(py):
    py.visit('https://google.com')
    py.get("[name='q']").type('puppies')
    py.get("[name='btnK']").submit()
    assert py.should().contain_title('puppies')

```

这个名命风格还真的有点像 cypress 呢！

```js
// cypress

describe('The Home Page', () => {
  it('successfully loads', () => {
    cy.visit('http://localhost:8080') // change URL to match your dev URL
    cy.get("[name='q']").type('puppies')
  })
})
```

__运行测试__

因为采用 pytest 框架编写，运行方式和 pytest 一致。

```bash
pytest test_google.py
```

### 评价

pylenium 对 selenium 的 API 进行了二次封装，并且 集成 pytest，大体思路和 seleniumbase 比较相似。

采用 json 文件来管理配置是一个不错的方式。

至于api的风格嘛，可以看出来是有意模仿 cypress，就是名命而已，没有好坏之分。

新手可以用他来写自动化吗？当然可以了。老手呢？爱用啥用啥，可以翻一翻他API设计上是否可取之处，自己设计一套 API 也可！


# 开发pytest插件

本章我们介绍如何开发pytest插件，在上一篇文章中我们介绍了4个python单元测试框架。大概分两类，一类是必须有类继承的，例如 `QTAF` 和 `unittest`， 另一类是可以没有类继承，例如`nose/nose2` 和 `pytest`。对于没有可以没有类继承的框架，开发难度会稍大一些。

## pytest扩展能力

如果我们需要给pytest增加额外的扩展能力，那么有三种方式。

### 1. 钩子函数

利用`conftest.py` 这个特殊的问题，可以创建钩子函数。

* 目录结构：

```shell
pytest_sample/
├── conftest.py
└── test_sample.py
```

在`conftest.py`文件中实现如下功能。

```py
import pytest

@pytest.fixture
def hello():
    return "hello 虫师"

```
定义一个函数`hello()`，并使用`pytest.fixture`装饰器对其进行装饰。fixture的概念我们前面已经做介绍。这里`fixture` 默认的级别为`function`，可以理解为被装饰的函数会在每个功能前被执行。

然后，在`test_sample.py` 测试文件中调动钩子函数。

```py
# 调用钩子函数hello
def test_case(hello):
    print("hello:", hello)
    assert hello == "hello 虫师"
```

在测试用例中钩子函数`hello()`作为测试用例的参数`hello` 被调用了。 断言 `hello`函数返回的结果是否为“hello 虫师”

* 执行用例：

```shell
> pytest -vs test_sample.py
================================= test session starts ===========================
collected 1 item

test_sample.py::test_case hello: hello 虫师
PASSED

================================== 1 passed in 2.61s =============================
```

### 2. 用例装饰器

我们比较常用的用例装饰是`parametrize`，用法如下。

```py
import pytest


@pytest.mark.parametrize(
    'a, b', 
    [
        (1, 2),
        (2, 3),
        (3, 4),
    ]
)
def test_add(a, b):
    print(f'a:{a}, b:{b}')
    assert a + 1 == b
```

使用`pytest.mark.parametrize()`装饰器，装饰`test_add()`测试用例。定义a和b为参数变量，每次取一组数据进行测试。

* 运行结果

```shell
> pytest -vs test_sample.py
================================= test session starts ===========================
collected 3 items

test_sample.py::test_add[1-2] a:1, b:2
PASSED
test_sample.py::test_add[2-3] a:2, b:3
PASSED
test_sample.py::test_add[3-4] a:3, b:4
PASSED

================================== 3 passed in 2.51s =============================
```


### 3.命令行参数

通过`pytest` 命令执行用例的时候作为参数传值。 以`pytest`的扩展插件`pytest-base-url` 为例。

* 安装

```shell
> pip install pytest-base-url
```

编写用例如下：

```py

def test_example(base_url):
    print("base_url:", base_url)
    assert "http" in base_url
```

这里同样用到了钩子函数`base_url`， 但base_url的参数定义是在执行用例的时候作为参数传入的。

* 运行测试

```shell
> pytest -vs test_sample.py --base-url https://www.baidu.com
================================= test session starts ===========================
collected 1 item

test_sample.py::test_example base_url: https://www.baidu.com
PASSED

================================== 1 passed in 2.51s =============================

```

## pytest扩展插件

### 实现pytest-hello插件
我么暂且称这个插件为`pytest-hello`。

创建`pytest_hello.py`文件，实现代码如下：

```python
import pytest
from typing import Any, Optional


def pytest_configure(config: Any) -> None:
    """
    register an additional marker
    """
    config.addinivalue_line(
        "markers", "env(name): mark test to run only on named environment"
    )


def pytest_runtest_setup(item: Any) -> None:
    """
    Called to perform the setup phase for a test item.
    """
    env_names = [mark.args[0] for mark in item.iter_markers(name="env")]
    if env_names:
        if item.config.getoption("--env") not in env_names:
            pytest.skip("test requires env in {!r}".format(env_names))


@pytest.fixture(scope="function")
def hello(hello_name: str) -> str:
    """
    hello Hook function
    """
    return f"hello, {hello_name}"


@pytest.fixture(scope="function")
def hello_name(pytestconfig: Any) -> Optional[str]:
    """
    hello_name Hook function
    """
    names = pytestconfig.getoption("--hello")
    if len(names) == 0:
        return "虫师"
    if len(names) == 1:
        return names[0]
    return names[0]


def pytest_addoption(parser: Any) -> None:
    """
    Add pytest option
    """
    group = parser.getgroup("hello", "Hello")
    group.addoption(
        "--env",
        action="store",
        default=[],
        help="only run tests matching the environment {name}.",
    )
    group.addoption(
        "--hello",
        action="append",
        default=[],
        help="hello {name}",
    )

```

__主要代码说明：__

1. 在函数`pytest_addoption()`中，增加一个命令行组`Hello`，添加两个参数`--env`和`--hello`。

2. 在钩子函数`hello_name()`中， 通过`pytestconfig` 获取`--hello` 参数值，如果为空默认值为“虫师”，如果为一个值或多个值取第1个。

3. 在钩子函数`hello()`中， 获取`hello_name()`中返回的值，并加上"hello, " 的前缀返回。

4. 在函数`pytest_configure`中，添加markrs扩展`env()`，获取环境名称。

5. 在函数`pytest_runtest_setup()`中，获取markrs中的`env()`的值，判断是否等于`--env` 参数值，如果不相等，跳过测试用例，否则执行用例。


对于`pytest-hello`项目，需要创建`setup.py`文件进行安装，在后面的章节会介绍该文件如何设置。现在，参考github上的介绍，安装`pytest-hello`插件。

github:https://github.com/defnngj/pytest-hello

### pytest-hello使用

当你安装好`pytest-hello`后，使用通过`pytest --help`查看帮助信息。

```shell
> pytest --help
...

Hello:
  --env=ENV             only run tests matching the environment {name}.
  --hello=HELLO         hello {name}
...
```

在`test_sample.py`测试文件中，编写测试用例：

```python
import pytest


@pytest.mark.env("test")
def test_case(hello):
    print("hello:", hello)
    assert "hello" in hello
```

`pytest.mark.env()`装饰器是`pytest-hello`实现的markrs实现的扩展方法。`hello`同样是`pytest-hello`实现的钩子函数。


__执行测试用例：__

1. 不设置`--env`参数或设置参数值非`test`，跳过用例。
 
```shell
> pytest -vs test_sample.py --env dev

collected 1 item
test_sample.py::test_case SKIPPED (test requires env in ['test'])
```

2. 设置`--env`参数值为`test`， 同时未设置`--hello` 参数，默认值为“虫师”
 
```shell
> pytest -vs test_sample.py --env test

collected 1 item

test_sample.py::test_case hello: hello, 虫师
PASSED
```

3. 设置`--env`参数值为`test`, 同时设置`--hello` 参数值为`jack`。

```shell
> pytest -vs test_sample.py --env test --hello jack

collected 1 item

test_sample.py::test_case hello: hello, jack
PASSED
```

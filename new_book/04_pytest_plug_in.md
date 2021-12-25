## 如何开发pytest插件

本章我们介绍如何开发pytest插件，在上一篇文章中我们介绍了4个python单元测试框架。大概分两类，一类是必须有类继承的，例如 `QTAF` 和 `unittest`， 另一类是可以没有类继承，例如`nose/nose2` 和 `pytest`。对于没有可以没有类继承的框架，开发难度会稍大一些。

如果我们需要给pytest增加额外的扩展能力，那么有三种方式。

## 1. 钩子函数

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

## 2. 用例装饰器

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


## 3.命令行参数

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

### 设计pytest扩展

我么暂且称这个插件为`pytest-hello`, 参考项目：

https://github.com/defnngj/pytest-hello


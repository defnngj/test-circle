## 单元测试框架

### 测试框架基本能力

一款测试框架应该具备以下基本能力：

* test case: 从程序层面只有`类`、`方法`、`函数`等，如何定义一条`测试用例`？不同的测试框架有不同的规则，例如大部分测试框架以`test`开头的`方法/函数` 识别为一条用例。

* test fixture: 在运行测试用例前后往往需要完成一些前置/后置的工作，例如用例执行之前需要构造测试数据，用例执行之后需要清除测试数据等，这些工作就可以在测试fixture中完成。

* test suite: 当框架需要执行用例之前需要查找并添加用例到一个集合中，我们一般称之为测试套件。

* test runner: 测试运行器主要用例执行测试套件中的用例，并生成日志或报告。

* assert: 断言主要用于检查用例的结果是否正确，从而判定用例成功/失败。

如果具备了以上能力，那么我们就可以视其为一款测试框架了。


### 常见单元测试框架

在Python语言中有很多优秀的单元测试框架，这里我们做个简单的介绍。

* unittest

unittest 单元测试框架是受到 JUnit 的启发，与其他语言中的主流单元测试框架有着相似的风格。其支持测试自动化，配置共享和关机代码测试。支持将测试样例聚合到测试集中，并将测试与报告框架独立。

相信大家对unittest并不陌生，他现在被纳入Python语言标准库，当你安装好Python就可以使用他了。

__简单示例__

```py
# test_ut.py
import unittest


class MyTest(unittest.TestCase):

    def test_case(self):
        self.assertEqual(2+2, 4)


if __name__ == '__main__':
    unittest.main()
```

运行结果：

```py
.
----------------------------------------------------------------------
Ran 1 test in 0.000s

OK
```

* QTAF

Testbase是所有QTA测试项目的基础，主要提供测试用例管理和执行、测试结果和报告、测试项目管理配置等功能。

QTAF是由腾讯开源的一款测试工具（框架），其设计风格与unittest比较相似。QTA是腾讯公司部门的缩写，我们也可以称其为Testbase。

```py
# qtaf_demo.py
from testbase.testcase import TestCase


class HelloTest(TestCase):
    """
    第一条用例
    """
    owner = "foo"
    status = TestCase.EnumStatus.Ready
    priority = TestCase.EnumPriority.Normal
    timeout = 1

    def run_test(self):
        self.start_step("第一个测试步骤")
        self.log_info("hello")
        self.assert_("检查计算结果", 2+2 == 4)


if __name__ == '__main__':
    HelloTest().debug_run()
```

有意思的是QTAF运行结果是中文的，这一点相对我们比较友好。

```shell
> python qtaf_demo.py
============================================================
测试用例:HelloTest 所有者:foo 优先级:Normal 超时:1分钟
============================================================
----------------------------------------
步骤1: 第一个测试步骤
INFO: hello
============================================================
测试用例开始时间: 2021-12-15 23:55:33
测试用例结束时间: 2021-12-15 23:55:33
测试用例执行时间: 00:00:0.02
测试用例步骤结果:  1:通过
测试用例最终结果: 通过
============================================================
```

github: https://github.com/Tencent/QTAF

* nose


Nose扩展了unittest使测试更容易。Nose2是nose的继承者，但nose2是一个新项目，不支持nose的所有功能。

Nose2的目的是扩展unittest，使测试更好、更容易理解。

可以直接使用`nose2`命令运行unittest编写的测试用例。

```
> nose2 -v
test_case (test_ut.MyTest) ... ok

----------------------------------------------------------------------
Ran 1 test in 0.000s

OK
```
这里不需要指定自动化测试文件，nose2按照`规则`查找当前目录下面的测试文件。

参数说明：

* -v ：可以看到日志的输出


我们也可以编写nose2风格的测试用例。

```py
# test_nose2.py
from nose2.tools import params

@params("Sir Bedevere", "Miss Islington", "Duck")
def test_is_knight(value):
    assert value.startswith('Sir')
```

这个例子用到了nose2提供的`params`参数化装饰测试用例，断言参数化数据是否以`Sir`开头。运行测试：

```py
> nose2 
.FF
===========================================
FAIL: test_nose2.test_is_knight:2
'Miss Islington'
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\test_nose2.py", line 6, in test_is_knight
    assert value.startswith('Sir')
AssertionError

===========================================
FAIL: test_nose2.test_is_knight:3
'Duck'
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\test_nose2.py", line 6, in test_is_knight
    assert value.startswith('Sir')
AssertionError

----------------------------------------------------------------------
Ran 3 tests in 0.000s

FAILED (failures=2)
```

github: https://github.com/nose-devs/nose2


* pytest

pytest框架使编写小型测试变得很容易，但可扩展到支持应用程序和库的复杂功能测试。

pytest已经变得非常流行，相信大家对他并不陌生。在nose2的项目中我们找到下面一句话。可见pytest非常优秀。

> 如果你是python测试的新手，我们鼓励你也考虑一下pytest，一个流行的测试框架。

需要说明的是pytest同样支持运行unittest编写的测试用例。

```shell
> pytest -v
=========== test session starts ===================
platform win32 -- Python 3.8.6, pytest-6.2.5, py-1.10.0, pluggy-0.13.1 -- C:\Python38\python.exe
cachedir: .pytest_cache
benchmark: 3.2.3 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=False warmup_iterations=100000)
metadata: {'Python': '3.8.6', 'Platform': 'Windows-10-10.0.22000-SP0', 'Packages': {'pytest': '6.2.5', 'py': '1.10.0', 'pluggy': '0.13.1'}, 'Plugins': {'allure-pytest': '2.8.40', 'base-url': '1.4.2', 'benchmark': '3.2.3', 'forked': '1.3.0', 'html': '3.1.1', 'metadata': '1.11.0', 'print': '0.3.0', 'rerunfailures': '9.1.1', 'xdist': '2.4.0'}, 'JAVA_HOME': 'C:\\Program Files\\Java\\jdk1.8.0_251', 'Base URL': ''}
rootdir: D:\ut_sample
plugins: allure-pytest-2.8.40, base-url-1.4.2, benchmark-3.2.3, forked-1.3.0, html-3.1.1, metadata-1.11.0, print-0.3.0, rerunfailures-9.1.1, xdist-2.4.0
collected 1 item

test_ut.py::MyTest::test_case PASSED               [100%]

============= 1 passed in 0.05s ================
```
pytest同样按照一定的`规则`默认查找当前目录下面的用例并执行。

参数说明：

* -v : 增加代码冗长，我们可以看到更多当前运行环境信息。

当然，如果使用pytest，我们应该按照他的风格编写测试用例。

```py
# test_sample.py
def test_answer():
    assert 3+1 == 5
```

可见他的风格与nose比较类似，可以直接创建测试`函数`。运行用例：

```shell
> pytest -q
F                                [100%]
====================== FAILURES =====================
_____________________ test_ans_______________________

    def test_answer():
>       assert 3+1 == 5
E       assert (3 + 1) == 5

test_pytest.py:4: AssertionError
============== short test summary info ==============
FAILED test_pytest.py::test_answer - assert (3 + 1) == 5
1 failed in 0.12s
```

这里特意设置断言的数值不相等，可以看到pytest为我们提供的错误日志。

参数说明：

* -q: 减少冗长。所以，你看不到任何环境相关信息。


github: https://github.com/pytest-dev/pytest



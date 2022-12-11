# 扩展unittest能力

unittest单元测试框架虽然使用比较简单，但他的功能不够强大，生态也相对没那么完善；因此有些功能就需要我们自己开发，来扩展他的能力。

## 用例依赖

在编写用例的时候不推荐你使用用例依赖，我们应该尽量消除用例的依赖；每条用例都应该是独立的，并且可以拿来单独执行。但是，有些时候我们并不能完全消除这些依赖。

用例的依赖分两种情况：

1. 依赖用例结果：根据被依赖用例的失败/错误/跳过，决定是否执行当前用例。
2. 依赖测试条件：根据一定的条件，决定是否依赖用例。

### 依赖用例结果

我们可以设计一个装饰器，来实现用例的依赖。

__功能代码:__

```py
import functools
from unittest import skipIf


def depend(case=None):
    """
    Use case dependency
    :param case
    :return:
    """
    def wrapper_func(test_func):

        @functools.wraps(test_func)
        def inner_func(self, *args):
            if case == test_func.__name__:
                raise ValueError(f"{case} cannot depend on itself")
            failures = str([fail_[0] for fail_ in self._outcome.result.failures])
            errors = str([error_[0] for error_ in self._outcome.result.errors])
            skipped = str([skip_[0] for skip_ in self._outcome.result.skipped])
            flag = (case in failures) or (case in errors) or (case in skipped)
            test = skipIf(flag, f'{case} failed  or  error or skipped')(test_func)
            try:
                return test(self)
            except TypeError:
                return None
        return inner_func
    return wrapper_func
```

__代码说明：__

> 关于python装饰器的实现说明请参考其他资料。

`test_func.__name__` 可以拿到被装饰的方法的名字，判断如果等于依赖的方法名，则抛出异常；直白点理解就是不能自己依赖自己。

`self._outcome.result` 可以获取`TextTestResult`类中已经运行的测试结果，这里要做的就是找出 失败(failures)、错误(errors)、跳过(skipped) 的用例。判断被依赖的用例是在这三类用例中。如果是则将依赖的用例设置为跳过。举个简单的例子，你的工作依赖同事小张，早会的时候，判断小张的工作情况，如果小张的工作失败了，那么将你的工作自动设置为忽略不做。

__使用例子:__

接下来通过例子演示`depend()` 装饰器的具体用法。

```py
# test_depend.py
import unittest
from extends.depend_extend import depend


class TestDepend(unittest.TestCase):

    def test_001(self):
        print("test_001")
        self.assertEqual(1+1, 3)

    @depend("test_001")
    def test_002(self):
        print("test_002")

    @depend("test_002")
    def test_003(self):
        print("test_003")

if __name__ == '__main__':
    unittest.main()
```

`test_002` 依赖于 `test_001` , `test_003`又依赖于`test_002`。当被依赖的用例，错误、失败、跳过，那么依赖的用例自动跳过。

这里有一个前提，`test_001` 一定要先被执行，如何保证被依赖的用例先执行？可以根据unittest查找用例的规则，通过测试方法命名上让用例先被执行；例如，同一个测试类下面，`test_a` 优先于 `test_b`执行，`test_1` 优先于`test_2`执行。

__执行结果:__

```shell
> python test_depend.py
test_001
Fss
======================================================================
FAIL: test_001 (__main__.TestDepend)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "test_depend.py", line 10, in test_001
    self.assertEqual(1+1, 3)
AssertionError: 2 != 3

----------------------------------------------------------------------
Ran 3 tests in 0.001s

FAILED (failures=1, skipped=2)
```

通过执行结果可以看出，被依赖用例`test_001` 断言失败，导致依赖用例`test_002`跳过，而`test_003`又依赖`test_002`，所以也做跳过处理。整个运行结果是：失败1条，跳过2条。

### 依赖测试结果

这种情况就不是依靠于被依赖用例的执行结果，被依赖的用例可以手动控制依赖的用例是否执行。同样拿前面的例子，你的工作依赖同事小张，早会的时候，判断小张的工作情况，小张的工作还未做完，但小张说你可以开展下一阶段的工作了，以小张的指导为准，而不是小张工作的成败。

__功能代码:__

```py

def if_depend(value):
    """
    Custom skip condition
    :param value
    :return:
    """
    def wrapper_func(function):
        def inner_func(self, *args, **kwargs):
            if not getattr(self, value):
                self.skipTest('Dependent use case not passed')
            else:
                function(self, *args, **kwargs)
        return inner_func
    return wrapper_func
```

__代码说明：__

`if_depend()` 装饰器的实现相对比较简单，通过判断`value`的结果：True/False，如果为 False，调用`self.skipTest()`跳过依赖的用例，否则，依赖的用例正常执行。

__使用例子:__

接下来通过例子演示`if_depend()` 装饰器的具体用法。

```py
# test_if_depend.py
import unittest
from extends.depend_extend import if_depend

class TestIfDepend(unittest.TestCase):
    depend_resule = True

    def test_001(self):
        TestIfDepend.depend_resule = False  # 修改depend_resule为 False

    @if_depend("depend_resule")
    def test_002(self):
        ...


if __name__ == '__main__':
    unittest.main()
```

在测试类中设置全局变量 depend_resule 的值为True，在`test_001` 中根据情况修改 `depend_resule`的值。 在`test_002`中通过`@if_depend()`取`depend_result`值进行装饰。

__执行结果:__

```shell
> python test_if_depend.py
.s
----------------------------------------------------------------------
Ran 2 tests in 0.000s

OK (skipped=1)
```

通过执行结果可以看到，在`test_001` 中修改 `depend_resule`的值为False，从而导致`test_002`用例跳过。

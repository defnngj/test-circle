# 用例分类标签

一般情况下，我们对用例的划分是按照功能模块的维度划分的；例如一个测试平台一般分为：登录/注册，项目管理、用例管理、任务管理等。编写自动化测试用例也是按照这个维护创建对应的目录结构。然后在执行的时候也是按照功能模块来执行。

除此之外，同一模块中的用例也有重要程度的维度，例如 登录用例，合法用户登录成功的用例就非常重要；项目管理的用例，合法数据创建项目成功的用例就非常重要。这都都是验证功能是否可用的最基本的用例。那么，我们在执行用例的时候，有可能为了节约执行时间而选择只运行这一类最基本的用例。而用例的存放方式只能以一种维度保存：功能模块 or 重要程度。这就引申出一个问题，如何按照不同的维度找出某一类用例，并执行他们？给用例打上不同的标签是一种解决方案。

为了让unittest支持多标签的功能，需要完成两个功能：

1. 实现用例标签装饰器。
2. 重写unittest的TextTestRunner类部分方法，识别用例标签。

__目录结构:__

```shell
├───extends
│   └───label_extend.py
├───runner
│   └───runner.py
└───test_label.py
```

__功能代码:__

1. 实现用例标签装饰器

```py
# label_extend.py


def label(*labels):
    """
    测试用例分类标签

    Usage:
        class MyTest(unittest.TestCase):
            
            @label('quick')
            def test_foo(self):
                pass
    """

    def inner(cls):
        # 类添加标签
        cls._labels = set(labels) | getattr(cls, '_labels', set())
        return cls

    return inner
```

__代码说明：__

如果通过`label()` 装饰器给类/方法设置了标签，那么使用 `set()` 类的标签合集。

2. 重写TextTestRunner类

```py
# runner.py
import unittest
import functools


class MyTestRunner(unittest.TextTestRunner):
    """继承&重写 TextTestRunner 类"""

    def __init__(self, *args, **kwargs):
        """
        增加属性：
        * 黑名单 blacklist 
        * 白名单 whitelist
        """
        self.whitelist = set(kwargs.pop('whitelist', []))
        self.blacklist = set(kwargs.pop('blacklist', []))

        super(MyTestRunner, self).__init__(*args, **kwargs)

    @classmethod
    def test_iter(cls, suite):
        """
        遍历测试套件，生成单个测试
        """
        for test in suite:
            if isinstance(test, unittest.TestSuite):
                for t in cls.test_iter(test):
                    yield t
            else:
                yield test

    def run(self, testlist):
        """
        运行给定的测试用例或测试套件。
        """
        suite = unittest.TestSuite()

        # 在测试列表中添加每个测试，必要时使用跳过机制
        for test in self.test_iter(testlist):
            # 获取用是否添加了标签，以及标签是否在 白名单 或 黑名单中
            skip = bool(self.whitelist)
            test_method = getattr(test, test._testMethodName)
            test_labels = getattr(test, '_labels', set()) | getattr(test_method, '_labels', set())
            if test_labels & self.whitelist:
                skip = False
            if test_labels & self.blacklist:
                skip = True

            if skip:
                # 针对跳过的用例，通过 skip 替换原始方法
                @functools.wraps(test_method)
                def skip_wrapper(*args, **kwargs):
                    raise unittest.SkipTest('label exclusion')
                skip_wrapper.__unittest_skip__ = True
                if len(self.whitelist) >= 1:
                    skip_wrapper.__unittest_skip_why__ = f'label whitelist {self.whitelist}'
                if len(self.blacklist) >= 1:
                    skip_wrapper.__unittest_skip_why__ = f'label blacklist {self.blacklist}'
                setattr(test, test._testMethodName, skip_wrapper)

            suite.addTest(test)

        super(MyTestRunner, self).run(suite)
```

__代码说明：__

这部分代码比较复杂，代码中必要的位置增加了注释。整体思路如下：

首先，在类`__init__()`初始化方法中增加 黑名单和白名单。

* 黑名单：只跳过黑名单上的用例。
* 白名单：只运行白名单上的用例。

然后，新增加`test_iter()` 方法，遍历测试套件，生成测试用例。

最后，重写`run()`方法，遍历`test_iter()` 生成的用例，获取类/方法的标签，如果标签在白名单中，不跳过用例（skip=False）； 如果标签的在黑名单中，则跳过用例(skip=True)。 针对跳过的用例，通过skip 替换原始的方法。

__使用实例：__

```py
# test_label.py
import unittest
from extends.label_extend import label
from runner.runner import MyTestRunner


class MyTest(unittest.TestCase):

    @label("base")
    def test_label_base(self):
        self.assertEqual(1+1, 2)

    @label("slow")
    def test_label_slow(self):
        self.assertEqual(1, 2)

    def test_no_label(self):
        self.assertEqual(2+3, 5)


if __name__ == '__main__':
    suit = unittest.TestSuite()
    suit.addTests([
        MyTest("test_label_base"),
        MyTest("test_label_slow"),
        MyTest("test_no_label")
    ])
    runner = MyTestRunner(whitelist=["base"], verbosity=2)  # 白名单
    # runner = MyTestRunner(blacklist=["slow"], verbosity=2)    # 黑名单
    runner.run(suit)
```

分别实现三条用例，设置前2条分别设置不同的标签，以及第3条不设置标签。

* 设置白名单执行

```shell
> python test_label.py
test_label_base (__main__.MyTest) ... ok
test_label_slow (__main__.MyTest) ... skipped "label whitelist {'base'}"
test_no_label (__main__.MyTest) ... skipped "label whitelist {'base'}"

----------------------------------------------------------------------
Ran 3 tests in 0.000s

OK (skipped=2)
```

因为第1条用例设置了白名单标签，所以被执行，其他用例跳过。

* 设置黑名单执行

> 注释白名单，取消注释黑名单

```shell
python test_label.py
test_label_base (__main__.MyTest) ... ok
test_label_slow (__main__.MyTest) ... skipped "label blacklist {'slow'}"
test_no_label (__main__.MyTest) ... ok

----------------------------------------------------------------------
Ran 3 tests in 0.001s

OK (skipped=1)
```

因为第2条用例在黑名单生，所以跳过，其他用例正常执行。

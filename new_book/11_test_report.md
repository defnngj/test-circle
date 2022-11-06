# 定制开发测试报告

这是一个看脸的时代，一款自动化测试工具和框架是否能够吸引到用户使用，主要看的测试报告是否好看。那么如果我们想为测试框架设计测试报告，应该怎么入手呢？你需要考虑以下问题。

* 如何从测试框架中提取到测试数据。例如，每条用例的名称、描述、执行结果（成功/失败/错误/跳过）等。

* HTML/CSS/JavaScript前端开发技术。是的，我们需要掌握一定的前端开发技术，从而才能设计出HTML类型的报告。

* XML/JSON: 一般这两种格式的报告用于保存测试结果数据，便于解析。例如，解析保存到数据库，便于在测试平台上展示。

## 基于unittest重写测试报告

我们知道unittest没有生成HTML报告的功能，如果我们要基于unittest生成测试报告，就不得对他的两个类进行重写。

* `unittest.TestResult`：这个类主要用于记录每个用例的结果。
* `unittest.TextTestRunner`: 这个类主要用于运行测试。

HTMLTestRunenr 对于基于unittest单元测试框架生成HTML测试报告提供思路。后续，我们看到了各式各样定时版本的HTMLTestRunner，我们这里同样借鉴 HTMLTestRunenr的代码。

Github地址:https://github.com/tungwaiyip/HTMLTestRunner

原项目代码是HTML代码和python代码混合在一起的，而且整个项目代码写在一个文件当中，阅读起来有一定难度。为了帮助你理解，我做了大量删减和修改，只保留基本的功能。


```shell
├───jsonrunner  
│   ├───result.py
│   └───runner.py
├───test_jsonrunner.py
└───result.json
```

#### 继承重写 `unittest.TestResult` 类

```py
# jsonrunner/result.py
import sys
from unittest import TestResult


class _TestResult(TestResult):
    """
    继承 unittest.TestResult 类，重写通过/失败/错误/跳过等方法
    """

    def __init__(self, verbosity=1):
        TestResult.__init__(self)
        self.success_count = 0
        self.failure_count = 0
        self.error_count = 0
        self.skip_count = 0
        self.verbosity = verbosity
        self.result = []

    def startTest(self, test):
        TestResult.startTest(self, test)

    def addSuccess(self, test):
        self.success_count += 1
        TestResult.addSuccess(self, test)
        self.result.append((0, test, ''))
        if self.verbosity > 1:
            sys.stderr.write('ok')
            sys.stderr.write(str(test))
            sys.stderr.write('\n')
        else:
            sys.stderr.write('.'+str(self.success_count))

    def addFailure(self, test, err):
        self.failure_count += 1
        TestResult.addFailure(self, test, err)
        _, _exc_str = self.failures[-1]
        self.result.append((1, test, _exc_str))
        if self.verbosity > 1:
            sys.stderr.write('F')
            sys.stderr.write(str(test))
            sys.stderr.write('\n')
        else:
            sys.stderr.write('F')

    def addError(self, test, err):
        self.error_count += 1
        TestResult.addError(self, test, err)
        _, _exc_str = self.errors[-1]
        self.result.append((2, test, _exc_str))
        if self.verbosity > 1:
            sys.stderr.write('E')
            sys.stderr.write(str(test))
            sys.stderr.write('\n')
        else:
            sys.stderr.write('E')

    def addSkip(self, test, reason):
        self.skip_count += 1
        TestResult.addSkip(self, test, reason)
        self.result.append((3, test, reason))
        if self.verbosity > 1:
            sys.stderr.write('S')
            sys.stderr.write(str(test))
            sys.stderr.write('\n')
        else:
            sys.stderr.write('S')
```

__代码说明：__

首先 `_TestResult` 类继承`unittest.TestResult` 类。

然后，主要重写`addSuccess()`、`addFailure()`、`addError()`、`addSkip()` 四个方法，对应用添加用例的成功、失败、错误、跳过。

最后，把每种测试结果都记录到`self.result` 列表中。




### 实现 `JSONTestRunner` 类

实际上，我们要重写`unittest.TextTestRunner`类，从命名可以看出`unittest.TextTestRunner` 在运行的过程中只是简单的打印一些text文本。而我们现在要做的事情事可以把测试结果写入到一个JSON文件中。

```py
# jsonrunner/runner.py
import json
import datetime
from .result import _TestResult

# 定义用例类型
case_type = {
    0: "passed",
    1: "failure",
    2: "errors",
    3: "skipped",
}


class JSONTestRunner:
    """
    运行测试：生成JSON格式的测试结果
    """

    def __init__(self, output, verbosity=1):
        self.output = output
        self.verbosity = verbosity
        self.start_time = datetime.datetime.now()

    def run(self, test):
        """
        运行测试
        """
        result = _TestResult(self.verbosity)
        test(result)
        stop_time = datetime.datetime.now()
        case_info = self.test_result(result)
        with open(self.output, "w", encoding="utf-8") as json_file:
            json.dump(case_info, json_file)

        print(f"Time Elapsed: {self.start_time - stop_time}")
        return result

    def test_result(self, result):
        """
        解析测试结果
        """
        class_list = []
        sorted_result = self.sort_result(result.result)
        for cid, (cls, cls_results) in enumerate(sorted_result):
            # 统计类下面用例数据
            passed = failure = errors = skipped = 0
            for n, t, e in cls_results:
                if n == 0:
                    passed += 1
                elif n == 1:
                    failure += 1
                elif n == 2:
                    errors += 1
                else:
                    skipped += 1

            # 格式化类的描述信息
            if cls.__module__ == "__main__":
                name = cls.__name__
            else:
                name = "%s.%s" % (cls.__module__, cls.__name__)
            doc = cls.__doc__ and cls.__doc__.split("\n")[0] or ""
            desc = doc and '%s' % doc or name

            cases = []
            for tid, (n, t, e) in enumerate(cls_results):
                case_info = self.generate_case_data(cid, tid, n, t, e)
                cases.append(case_info)

            class_list.append({
                "desc": desc,
                "count": passed + failure + errors + skipped,
                "pass": passed,
                "fail": failure,
                "error": errors,
                "skipped": skipped,
                "cases": cases
            })

        return class_list

    @staticmethod
    def sort_result(result_list):
        """
        unittest运行用例没有特定的顺序，
        这里将测试用例按照测试类分组
        """
        rmap = {}
        classes = []
        for n, t, e in result_list:
            cls = t.__class__
            if not cls in rmap:
                rmap[cls] = []
                classes.append(cls)
            rmap[cls].append((n, t, e))
        r = [(cls, rmap[cls]) for cls in classes]
        return r

    @staticmethod
    def generate_case_data(cid, tid, n, t, e):
        """
        生成测试用例数据
        """
        tid = (n == 0 and "p" or "f") + f"t{cid +1}.{tid+1}"
        name = t.id().split('.')[-1]
        doc = t.shortDescription() or ""

        case = {
            "number": tid,
            "name": name,
            "doc": doc,
            "result": case_type.get(n),
            "error": e
        }

        return case

```

__代码说明：__

解析用例的过程比较复杂，虽然我已经尽力做了简化，但仍然需要 100多行的代码实现。

首先，在`__init__()` 初始化方法中，通过`output`参数接收一个文件名，用于保存JSON格式的结果。

其次，在`run()` 方法中，通过`test`参数接收组装测试用例的测试套件。 调用 `_TestResult` 类记录测试的运行结果。

最后，把结果丢给`self.test_result()`方法进行解析，整个解析的过程主要围绕两个维度：测试类和测试用例。每个维度又包含不同的信息。
 * 测试类：类名、类描述，统计类下面用例数（成功/失败/错误/跳过）。
 * 测试用例：方法名、方法描述，结果、错误信息。

最终，将这些数据组装成列表&字典，并转换成JSON格式进行保存。


### 测试用例

通过测试用例验证实现的`JSONTestRunner` 类是否可用。

```python
# test_jsonrunner.py
import unittest
from jsonrunner.runner import JSONTestRunner


class TestDemo(unittest.TestCase):
    """Test Demo class"""

    def test_pass(self):
        """pass case"""
        self.assertEqual(5, 5)

    def test_fail(self):
        """fail case"""
        self.assertEqual(5, 6)

    def test_error(self):
        """error case"""
        self.assertEqual(a, 6)

    @unittest.skip("skip case")
    def test_skip(self):
        """skip case"""
        ...


if __name__ == '__main__':
    suit = unittest.TestSuite()
    suit.addTests([
        TestDemo("test_pass"),
        TestDemo("test_skip"),
        TestDemo("test_fail"),
        TestDemo("test_error")
    ])

    runner = JSONTestRunner(output="./result.json")
    runner.run(suit)
```

__代码说明：__

首先，创建`TestDemo`类，分别实现测试结果成功/失败/错误/跳过4条用例。

其次，调用`unittest.TestSuite`测试套件组装测试用例。

最后，调用`JSONTestRunner`类，指定测试报告路径；通过`run()`方法运行测试套件中的用例。

__查看json测试结果：__

打开`result.json` 文件，查看结果。

```json
[
  {
    "desc": "TestDemo: Test Demo class",
    "count": 4,
    "pass": 1,
    "fail": 1,
    "error": 1,
    "skipped": 1,
    "cases": [
      {
        "number": "pt1.1",
        "name": "test_pass",
        "doc": "pass case",
        "result": "passed",
        "error": ""
      },
      {
        "number": "ft1.2",
        "name": "test_skip",
        "doc": "skip case",
        "result": "skipped",
        "error": "skip case"
      },
      {
        "number": "ft1.3",
        "name": "test_fail",
        "doc": "fail case",
        "result": "failure",
        "error": "Traceback (most recent call last):\n  File \".\\test_jsonrunner.py\", line 20, in test_fail\n    self.assertEqual(5, 6)\nAssertionError: 5 != 6\n"
      },
      {
        "number": "ft1.4",
        "name": "test_error",
        "doc": "error case",
        "result": "errors",
        "error": "Traceback (most recent call last):\n  File \".\\test_jsonrunner.py\", line 24, in test_error\n    self.assertEqual(a, 6)\nNameError: name 'a' is not defined\n"
      }
    ]
  }
]
```


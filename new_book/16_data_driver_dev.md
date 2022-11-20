## 开发数据驱动

通过上一节的学习，我们对 `parameterized` 和 `ddt` 的使用有了一定的了解，不过，这两个数据驱动库都有一些的不足:

* `parameterized` 不支持数据文件，对于简单的数据可以通过 `@parameterized.expand()` 装饰器在代码中定义，对于复杂的数据，或者大量的测试数据(例如我们在做接口测试时，数据文件都会达到几百行) 如果都在代码中管理显然不够优雅的。

* `ddt` 显然要比`parameterized` 强大一些；支持更多的数据格式；支持数据驱动文件（YAML/JSON）。但是，在使用的时候需要对类加`@ddt`装饰；装饰测试用例要用到`@data` 和`@unpack`， 写法上不够简洁。再者，数据驱动文件不支持CSV、Excel、XML等数据文件。

基于上面两个库的不足，所以我们需要封装自己的数据驱动库来弥补这些不足。


## 实现 @data 装饰器

我们可以`parameterized`的基础上进行开发。`parameterized` 核心文件代码大概 600 行，我们可以花一些时间来阅读这部分代码，对于我们深入理解数据驱动的实现有很大帮助。

我们会发现`parameterized` 对unittest框架的支持是个二等公民，因为装饰器的写法是`@parameterized.expand()`，即放到一个`expand()`方法里面的。我们首先可以将这个方法剥离出来重写。


```py
# extend/parameterized_extend.py
import warnings
from parameterized.parameterized import inspect
from parameterized.parameterized import parameterized
from parameterized.parameterized import skip_on_empty_helper
from parameterized.parameterized import reapply_patches_if_need
from parameterized.parameterized import delete_patches_if_need
from parameterized.parameterized import default_doc_func
from parameterized.parameterized import default_name_func
from parameterized.parameterized import wraps


def data(input, name_func=None, doc_func=None, skip_on_empty=False, **legacy):
    """
    重写 parameterized.expend()方法
    """

    if "testcase_func_name" in legacy:
        warnings.warn("testcase_func_name= is deprecated; use name_func=",
                      DeprecationWarning, stacklevel=2)
        if not name_func:
            name_func = legacy["testcase_func_name"]

    if "testcase_func_doc" in legacy:
        warnings.warn("testcase_func_doc= is deprecated; use doc_func=",
                      DeprecationWarning, stacklevel=2)
        if not doc_func:
            doc_func = legacy["testcase_func_doc"]

    doc_func = doc_func or default_doc_func
    name_func = name_func or default_name_func

    def parameterized_expand_wrapper(f, instance=None):
        frame_locals = inspect.currentframe().f_back.f_locals

        parameters = parameterized.input_as_callable(input)()

        if not parameters:
            if not skip_on_empty:
                raise ValueError(
                    "Parameters iterable is empty (hint: use "
                    "`parameterized.expand([], skip_on_empty=True)` to skip "
                    "this test when the input is empty)"
                )
            return wraps(f)(skip_on_empty_helper)

        digits = len(str(len(parameters) - 1))
        for num, p in enumerate(parameters):
            name = name_func(f, "{num:0>{digits}}".format(digits=digits, num=num), p)
            # If the original function has patches applied by 'mock.patch',
            # re-construct all patches on the just former decoration layer
            # of param_as_standalone_func so as not to share
            # patch objects between new functions
            nf = reapply_patches_if_need(f)
            frame_locals[name] = parameterized.param_as_standalone_func(p, nf, name)
            frame_locals[name].__doc__ = doc_func(f, num, p)

        # Delete original patches to prevent new function from evaluating
        # original patching object as well as re-constructed patches.
        delete_patches_if_need(f)

        f.__test__ = False

    return parameterized_expand_wrapper

```

__代码说明：__

首先，把`parameterized`库中`parameterized`类下面的`expend`方法拷贝出来，定义成一个函数，并重命名为`data`。

然后，找到函数中依赖的方法，直接从`parameterized`库中的相关文件中导入。

__使用例子:__

编写测试用例，验证`data`函数是否可用。

```py
# parameterized_expend_demo.py
import unittest
from extend.parameterized_extend import data


class ParamTestCase(unittest.TestCase):

    @data([
        ("2 and 3", 2, 3, 5),
        ("10 and 20", 10, 20, 30),
        ("hello and word", "hello", "world", "helloworld"),
    ])
    def test_add(self, _, a, b, expected):
        self.assertEqual(a + b, expected)


if __name__ == '__main__':
    unittest.main(verbosity=1)
```

通过例子可以看出，与之前的用法并无太大差别，这里使用新封装的`@data()`装饰器装饰测试方法。


__运行结果：__

```shell
> python .\parameterized_expend_demo.py

test_add_0_2_and_3 (__main__.ParamTestCase) ... ok
test_add_1_10_and_20 (__main__.ParamTestCase) ... ok
test_add_2_hello_and_word (__main__.ParamTestCase) ... ok

----------------------------------------------------------------------
Ran 3 tests in 0.001s

OK
```


## 基于 @data 支持dict格式

目前`@data` 装饰器仅支持list和tuple两种数据格式，虽然这两种数据的格式比较简单，但是对于数据的描述能力比较弱。

```py
@data([
    ("case1", "", "123"),
    ("case2", "user", ""),
    ("case3", "user", "123"),
])
```

从上面的例子可以看出，单看tuple中的每一列数据，我们很难理解每个数据所代表的含义。如果把它变成dict的key来描述每个字段的含义，那么理解起来就会变得更加容易。

```py
@data([
    {"scene": "username_is_null", "username": "", "password": "123"},
    {"scene": "password_is_null", "username": "user", "password": ""},
    {"scene": "login_success", "username": "user", "password": "123"},
])
```

现在需求有了，我们要做的就是去修改`data()`函数，让它可以支持字典格式的数据。

```py

def check_data(list_data: list) -> list:
    """
    检查数据格式，如果是dict转化为list.
    """
    if isinstance(list_data, list) is False:
        raise TypeError("The data format is not `list`.")
    if len(list_data) == 0:
        raise ValueError("The data format cannot be `[]`.")
    if isinstance(list_data[0], dict):
        test_data = []
        for data_ in list_data:
            line = []
            for d in data_.values():
                line.append(d)
            test_data.append(line)
        return test_data

    return list_data


def data(input, name_func=None, doc_func=None, skip_on_empty=False, **legacy):
    """
    重写 parameterized.expend()方法
    """

    input = check_data(input)
    ...
```

__代码说明：__

首先，实现`check_data()` 函数，进行数据检查，如果判断传入的数据类型是 dict，那么通过`values()`找出dict中的每个value值，将它们拼装到一个二维列表当中，最后将整个列表返回。

然后，在`data()` 函数中先调用`check_data()` 函数进行判断。

__使用例子:__

编写测试用例，验证上面的改动是否有效。

```py
# parameterized_expend_demo.py
import unittest
from extend.parameterized_extend import data


class ParamTestCase(unittest.TestCase):

    @data([
        {"scene": "username_is_null", "username": "", "password": "123"},
        {"scene": "password_is_null", "username": "user", "password": ""},
        {"scene": "login_success", "username": "user", "password": "123"},
    ])
    def test_login(self, name, username, password):
        print(f"case: {name}, username: '{username}' password: '{password}'")


if __name__ == '__main__':
    unittest.main(verbosity=1)
```

__运行结果：__

```shell
> python .\parameterized_expend_demo.py

case: username_is_null, username: '' password: '123'
case: password_is_null, username: 'user' password: ''
case: login_success, username: 'user' password: '123'
...
----------------------------------------------------------------------
Ran 3 tests in 0.001s

OK
```
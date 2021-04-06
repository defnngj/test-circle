# 代码性能分析

上一篇文章我们介绍了[基准测试](./benchmarks_test.md)，通过基准测试可以发现程序变慢了，那么是因为什么原因导致性能变慢的，需要进一步做代码性能分析。python同样提供了性能分析工具。


## cProfile

cProfile是python默认的性能分析器，他只测量CPU时间，并不关心内存消耗和其他与内存相关联的信息。

```py
from time import sleep
import random


def random_list(start, end, length):
    """
    生成随机列表
    :param start: 随机开始数
    :param end: 随机结束数
    :param length: 列表长度
    """
    data_list = []
    for i in range(length):
        data_list.append(random.randint(start, end))
    return data_list


def bubble_sort(arr):
    """
    冒泡排序: 对列表进行排序
    :param arr 列表
    """
    n = len(arr)
    sleep(1)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


if __name__ == '__main__':
    get_data_list = random_list(1, 99, 10)

    import cProfile
    cProfile.run('bubble_sort({})'.format(get_data_list))
```

继续使用上一篇文章中的例子，引用`cProfile`模块，`run()`方法参数说明。

`run(statement, filename=None, sort=-1)`

* statement: 需要测试的代码或者函数（函数名）
* fielname: 结果保存的位置， 默认为stdout
* sort: 结果排序方法，常用的有`cumtime`: 累积时间， `name`: 函数名， `line`: 行号

为了使结果统计出耗时部分，我们加了`sleep`，结果如下：

```shell
❯ python demo.py
         6 function calls in 1.004 seconds

   Ordered by: standard name

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000    1.004    1.004 <string>:1(<module>)
        1    0.000    0.000    1.004    1.004 demo.py:19(bubble_sort)
        1    0.000    0.000    1.004    1.004 {built-in method builtins.exec}
        1    0.000    0.000    0.000    0.000 {built-in method builtins.len}
        1    1.004    1.004    1.004    1.004 {built-in method time.sleep}
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
```

* `6 function calls in 1.004 seconds`  6个函数调用被监控，耗时1.004秒。

* `ncalls` 函数被调用的次数。如果这一列有两个值，就表示有递归调用，第二个值是原生调用次数，第一个值是总调用次数。

* `tottime` 函数内部消耗的总时间。（可以帮助优化）

* `percall` 是tottime除以ncalls，一个函数每次调用平均消耗时间。

* `cumtime` 之前所有子函数消费时间的累计和。

* `filename:lineno(function)` 被分析函数所在文件名、行号、函数名。


## line_profiler

`line_profiler` 可以提供有关时间是如何在各行之间分配的信息，直白一点就是给出程序每行的耗时，在无法确定哪行语句最浪费时间，这很有用。

line_profiler是一个第三方模块，需要安装。

https://github.com/pyutils/line_profiler

```py
from time import sleep
import random


def random_list(start, end, length):
    """
    生成随机列表
    :param start: 随机开始数
    :param end: 随机结束数
    :param length: 列表长度
    """
    data_list = []
    for i in range(length):
        data_list.append(random.randint(start, end))
    return data_list


@profile
def bubble_sort(arr):
    """
    冒泡排序: 对列表进行排序
    :param arr 列表
    """
    n = len(arr)
    sleep(1)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


if __name__ == '__main__':
    get_data_list = random_list(1, 99, 10)
    bubble_sort(get_data_list)
```

给需要监控的函数加上`@profile` 装饰器。通过`kernprof`命令运行文件（安装完line_profiler生成的命令）。

参数说明：

* `-l`：以使用函数line_profiler

* `-v`：以立即将结果打印到屏幕

运行结果：

```shell
kernprof -l -v demo.py
Wrote profile results to demo.py.lprof
Timer unit: 1e-06 s

Total time: 1.00416 s
File: demo.py
Function: bubble_sort at line 18

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    18                                           @profile
    19                                           def bubble_sort(arr):
    20                                               """
    21                                               冒泡排序: 对列表进行排序
    22                                               :param arr 列表
    23                                               """
    24         1          8.0      8.0      0.0      n = len(arr)
    25         1    1004030.0 1004030.0    100.0      sleep(1)
    26        11         15.0      1.4      0.0      for i in range(n):
    27        55         44.0      0.8      0.0          for j in range(0, n - i - 1):
    28        45         41.0      0.9      0.0              if arr[j] > arr[j + 1]:
    29        20         21.0      1.1      0.0                  arr[j], arr[j + 1] = arr[j + 1], arr[j]
    30         1          1.0      1.0      0.0      return arr
```

输出非常直观，分成了6列。

* `Line #`：运行的代码行号。
* `Hits`：代码行运行的次数。
* `Time`：代码行的执行时间，单位为微秒。
* `Per Hit`：Time/Hits。
* `% Time`：代码行总执行时间所占的百分比。
* `Line Contents`：代码行的内容。

只需查看`% Time`列，就可清楚地知道时间都花在了什么地方。


## 总结

性能测试分析站在项目层面是一个很庞大的话题，以前为测试工程师，关注的是性能工具的使用，以及用户维度的性能[1]；作为开发工程师，每个功能都是由一个个`函数/方法`组成，我们去分析每个`函数/方法`，甚至是每行`代码`的耗时，才能更好的进行代码层面的性能优化。

正如上文提到，大多数情况下我们不需要过多关注代码性能，我们在项目中大量使用别人的库和框架，大多时候也没有太多优化空间。但这并不代表我们完全不需要关注代码层面的性能。

优化方向：

* 业务优化：从业务方向进行优化，比如要查询三次数据库才能完成的操作，优化为查询两次数据库完成。
* 算法优化：在耗时的一些算法的进行优化，例如上文的冒泡排序，改用 python 提供的`sort()`函数，性能略优。


1. 用户维度的性能：这里指用户的一次搜索、一次登录、一次提交表单的耗时。

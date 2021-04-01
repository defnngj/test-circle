# 基准测试

__`基准测试`属于性能测试的一种，用于评估和衡量软件的性能指标。我们可以在软件开发的某个阶段通过`基准测试`建立一个已知的性能水平，称为"基准线"。当系统的软硬件环境发生变化之后再进行一次`基准测试`以确定那些变化对性能的影响。__ 这是基准测试最常见的用途。


Donald Knuth在1974年出版的《Structured Programming with go to Statements》提到：

> 毫无疑问，对效率的片面追求会导致各种滥用。程序员会浪费大量的时间在非关键程序的速度上，实际上这些尝试提升效率的行为反倒可能产生很大的负面影响，特别是当调试和维护的时候。我们不应该过度纠结于细节的优化，应该说约97%的场景：过早的优化是万恶之源。
> 当然我们也不应该放弃对那关键3%的优化。一个好的程序员不会因为这个比例小就裹足不前，他们会明智地观察和识别哪些是关键的代码；但是仅当关键代码已经被确认的前提下才会进行优化。对于很多程序员来说，判断哪部分是关键的性能瓶颈，是很容易犯经验上的错误的，因此一般应该借助测量工具来证明。


虽然经常被解读为不需要关心性能，但是的少部分情况下（3%）应该观察和识别关键代码并进行优化。

## 基准(benchmarking)测试工具 

python中提供了非常多的工具来进行基准测试。

为了使演示的例子稍微有趣，我们来随机生成一个列表，并对列表中数字进行排序。

```py
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
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


if __name__ == '__main__':
    get_data_list = random_list(1, 99, 10)
    ret = bubble_sort(get_data_list)
    print(ret)
```


运行结果如下：
```shell
❯ python .\demo.py
[8, 16, 22, 31, 42, 58, 66, 71, 73, 91]
```

### timeit

timeit是python自带的模块，用来进行基准测试非常方便。

```py
if __name__ == '__main__':
    import timeit
    get_data_list = random_list(1, 99, 10)
    setup = "from __main__ import bubble_sort"
    t = timeit.timeit(
        stmt="bubble_sort({})".format(get_data_list),
        setup=setup
        )
    print(t)
```

运行结果：
```shell
❯ python .\demo.py
5.4201355
```

以测试`bubble_sort()`函数为例。`timeit.timeit()` 参数说明。

* stmt：需要测试的函数或语句，字符串形式.
* setup: 运行的环境，本例子中表示`if __name__ == '__main__':`.
* number: 执行的次数，省缺则默认是`1000000`次。所以你会看到运行`bubble_sort()` 耗时 5秒多。

### pyperf

https://github.com/psf/pyperf

pyperf 的用法与timeit比较类似，但它提供了更丰富结果。（注：我完全是发现了这个库才学习基准测试的）

```py
if __name__ == '__main__':
    get_data_list = random_list(1, 99, 10)

    import pyperf
    setup = "from __main__ import bubble_sort"
    runner = pyperf.Runner()
    runner.timeit(name="bubble sort",
                  stmt="bubble_sort({})".format(get_data_list),
                  setup=setup)

```

运行结果：
```shell
❯ python  .\demo.py -o bench.json
.....................
bubble sort: Mean +- std dev: 5.63 us +- 0.31 us
```

测试结果会写入`bench.json` 文件。可以使用`pyperf stats`命令分析测试结果。

```
❯ python -m pyperf stats bench.json
Total duration: 15.9 sec
Start date: 2021-04-02 00:17:18
End date: 2021-04-02 00:17:36
Raw value minimum: 162 ms
Raw value maximum: 210 ms

Number of calibration run: 1
Number of run with values: 20
Total number of run: 21

Number of warmup per run: 1
Number of value per run: 3
Loop iterations per value: 2^15
Total number of values: 60

Minimum:         4.94 us
Median +- MAD:   5.63 us +- 0.12 us
Mean +- std dev: 5.63 us +- 0.31 us
Maximum:         6.41 us

  0th percentile: 4.94 us (-12% of the mean) -- minimum
  5th percentile: 5.10 us (-9% of the mean)
 25th percentile: 5.52 us (-2% of the mean) -- Q1
 50th percentile: 5.63 us (+0% of the mean) -- median
 75th percentile: 5.81 us (+3% of the mean) -- Q3
 95th percentile: 5.95 us (+6% of the mean)
100th percentile: 6.41 us (+14% of the mean) -- maximum

Number of outlier (out of 5.07 us..6.25 us): 6
```

### pytest-benchmark

https://github.com/ionelmc/pytest-benchmark

pytest-benchmark是 pytest单元测试框架的一个插件。 单独编写单元测试用例：

```py
from demo import bubble_sort


def test_bubble_sort(benchmark):
    test_list = [5, 2, 4, 1, 3]
    result = benchmark(bubble_sort, test_list)
    assert result == [1, 2, 3, 4, 5]

```

需要注意：

1. 导入`bubble_sort()` 函数。
2. `benchmark` 作为钩子函数使用，不需要导入包。前提是你需要安装`pytest`和`pytest-benchmark`。
3. 为了方便断言，我们就把要排序的数固定下来了。

运行测试用例：

```
❯ pytest -q .\test_demo.py
.                                                                       [100%]

------------------------------------------------ benchmark: 1 tests -----------------------------------------------
Name (time in us)        Min       Max    Mean  StdDev  Median     IQR   Outliers  OPS (Kops/s)  Rounds  Iterations
-------------------------------------------------------------------------------------------------------------------
test_bubble_sort      1.6000  483.2000  1.7647  2.6667  1.7000  0.0000  174;36496      566.6715  181819           1
-------------------------------------------------------------------------------------------------------------------

Legend:
  Outliers: 1 Standard Deviation from Mean; 1.5 IQR (InterQuartile Range) from 1st Quartile and 3rd Quartile.
  OPS: Operations Per Second, computed as 1 / Mean
1 passed in 1.98s
```

加上 `--benchmark-histogram` 参数，你会得到一张图表

```
❯ pytest -q .\test_demo.py --benchmark-histogram
.                                                                                                                [100%]

------------------------------------------------ benchmark: 1 tests -----------------------------------------------
Name (time in us)        Min      Max    Mean  StdDev  Median     IQR    Outliers  OPS (Kops/s)  Rounds  Iterations
-------------------------------------------------------------------------------------------------------------------
test_bubble_sort      1.6000  53.9000  1.7333  0.3685  1.7000  0.0000  1640;37296      576.9264  178572           1
-------------------------------------------------------------------------------------------------------------------


Generated histogram: D:\github\test-circle\article\code\benchmark_20210401_165958.svg
```

图片如下：
![](/article/code/benchmark_20210401_165958.svg)

关于基准测试的工具还有很多，这里就不再介绍了。

经过基准测试发现程序变慢了，那么接下来需要做的就是代码性能分析了，我下篇再来介绍。




参考：
https://www.cnblogs.com/meishandehaizi/p/5863234.html
https://www.ituring.com.cn/book/tupubarticle/23109
https://books.studygolang.com/gopl-zh/ch11/ch11-05.html
http://www.51testing.com/html/20/n-816520.html
https://pytest-benchmark.readthedocs.io/en/latest/
https://github.com/psf/pyperf

http://www.starky.ltd/2020/12/22/python-design-patterns-factory-pattern/
https://www.py.cn/jishu/jichu/19193.html



## 分析profiling

经过基准测试发现程序变慢了，那么接下来需要做的就是代码性能分析了。
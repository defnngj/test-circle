# 基准测试

__`基准测试`属于性能测试的一种，用于评估和衡量软件的性能指标。我们可以在软件开发的某个阶段通过`基准测试`建立一个已知的性能水平，称为"基准线"。当系统的软硬件环境发生变化之后再进行一次`基准测试`以确定那些变化对性能的影响。__ 这是基准测试最常见的用途。


Donald Knuth在1974年出版的《Structured Programming with go to Statements》提到：

> 毫无疑问，对效率的片面追求会导致各种滥用。程序员会浪费大量的时间在非关键程序的速度上，实际上这些尝试提升效率的行为反倒可能产生很大的负面影响，特别是当调试和维护的时候。我们不应该过度纠结于细节的优化，应该说约97%的场景：过早的优化是万恶之源。
> 当然我们也不应该放弃对那关键3%的优化。一个好的程序员不会因为这个比例小就裹足不前，他们会明智地观察和识别哪些是关键的代码；但是仅当关键代码已经被确认的前提下才会进行优化。对于很多程序员来说，判断哪部分是关键的性能瓶颈，是很容易犯经验上的错误的，因此一般应该借助测量工具来证明。


参考：
https://www.cnblogs.com/meishandehaizi/p/5863234.html
https://www.ituring.com.cn/book/tupubarticle/23109
https://books.studygolang.com/gopl-zh/ch11/ch11-05.html
http://www.51testing.com/html/20/n-816520.html
https://pytest-benchmark.readthedocs.io/en/latest/
https://github.com/psf/pyperf

http://www.starky.ltd/2020/12/22/python-design-patterns-factory-pattern/

* 列子

```py
import random


def bubble_sort(arr):
    """
    冒泡排序
    :param 列表
    """
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


def random_list(start, stop, length):
    """
    生成随机列表
    :param
    """
    if length >= 0:
        length = int(length)
    start, stop = (int(start), int(stop)) if start <= stop else (int(stop), int(start))
    data_list = []
    for i in range(length):
        data_list.append(random.randint(start, stop))
    return data_list


if __name__ == '__main__':
    ret = random_list(1, 1000, 100)
    print(ret)
    ret2 = bubble_sort(ret)
    print(ret2)
```
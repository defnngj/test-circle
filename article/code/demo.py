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

@profile
def py_sort(arr):
    """
    python排序：对列表进行排序
    """
    sleep(1)
    arr.sort()
    return arr


if __name__ == '__main__':
    get_data_list = random_list(1, 99, 10)
    py_sort(get_data_list)

    # import timeit
    # setup = "from __main__ import bubble_sort"
    # t = timeit.timeit("bubble_sort({})".format(get_data_list), setup=setup)
    # print(t)

    # import pyperf
    # setup = "from __main__ import bubble_sort"
    # runner = pyperf.Runner()
    # runner.timeit(name="bubble sort",
    #               stmt="bubble_sort({})".format(get_data_list),
    #               setup=setup)

    # import cProfile
    # cProfile.run('bubble_sort({})'.format(get_data_list))

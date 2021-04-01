from demo import bubble_sort


def test_bubble_sort(benchmark):
    test_list = [5, 2, 4, 1, 3]
    result = benchmark(bubble_sort, test_list)
    assert result == [1, 2, 3, 4, 5]


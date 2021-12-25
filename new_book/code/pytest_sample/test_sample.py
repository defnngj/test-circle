
"""
调用钩子函数hello
"""
def test_case(hello):
    print("hello:", hello)
    assert hello == "hello"


"""
参数化
"""
import pytest

@pytest.mark.parametrize(
    'a, b', 
    [
        (1, 2),
        (2, 3),
        (3, 4),
    ]
)
def test_add(a, b):
    print(f'a:{a}, b:{b}')
    assert a + 1 == b


"""
命令行参数
"""
def test_example(base_url):
    print("base_url:", base_url)
    assert "http" in base_url

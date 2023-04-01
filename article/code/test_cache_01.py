import hashlib
from time import sleep, time
from functools import lru_cache


@lru_cache(None)
def login(username, password):
    """模拟登录生成token"""
    sleep(5)
    src = f'{username}.{password}'
    m = hashlib.md5()
    m.update(src.encode("utf-8"))
    token = m.hexdigest()

    return token


def test_case1():
    start = time()
    token = login("admin", "abc123")
    end = time()
    print(f"token: {token}, run time:{ end - start}")


def test_case2():
    start = time()
    token = login("admin", "abc123")
    end = time()
    print(f"token: {token}, run time:{ end - start}")


def test_case3():
    start = time()
    token = login("admin", "abc123")
    end = time()
    print(f"token: {token}, run time:{ end - start}")


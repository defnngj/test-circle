import hashlib
from time import sleep, time
from seldom.utils import cache


def login(username, password):
    """模拟登录生成token"""
    token = cache.get(username)
    # 如果有token 直接返回
    if token is not None:
        return token

    sleep(5)
    src = f'{username}.{password}'
    m = hashlib.md5()
    m.update(src.encode("utf-8"))
    token = m.hexdigest()
    # 写入 token
    cache.set({username: token})

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


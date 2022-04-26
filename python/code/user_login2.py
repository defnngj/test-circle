import json
import requests
from jmespath import search


def check_response(
        describe: str = "",
        status_code: int = 200,
        ret: str = None,
        check: dict = None,
        debug: bool = False):
    """
    checkout response data
    :param describe: interface describe
    :param status_code: http status code
    :param ret: return data
    :param check: check data
    :param debug: debug Ture/False
    :return:
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            func_name = func.__name__
            if debug is True:
                print(f"Execute {func_name} - args: {args}")
                print(f"Execute {func_name} - kwargs: {kwargs}")

            r = func(*args, **kwargs)
            flat = True
            if r.status_code != status_code:
                print(f"Execute {func_name} - {describe} failed: {r.status_code}")
                flat = False

            try:
                r.json()
            except json.decoder.JSONDecodeError:
                print(f"Execute {func_name} - {describe} failed：Not in JSON format")
                flat = False

            if debug is True:
                print(f"Execute {func_name} - response:\n {r.json()}")

            if flat is True:
                print(f"Execute {func_name} - {describe} success!")

            if check is not None:
                for expr, value in check.items():
                    data = search(expr, r.json())
                    if data != value:
                        print(f"Execute {func_name} - check data failed：{value}")
                        raise ValueError(f"{data} != {value}")

            if ret is not None:
                data = search(ret, r.json())
                if data is None:
                    print(f"Execute {func_name} - return {ret} is None")
                return data
            else:
                return r.json()

        return wrapper

    return decorator


class UserLogin:

    def __init__(self, username, password):
        self.username = username
        self.password = password

    @check_response("获取用户登录token", 200, ret="form.token", check={"headers.Host": "httpbin.org"}, debug=True)
    def get_token(self):
        """获取用户登录token"""
        url = "http://httpbin.org/post"

        data = {
            "username": self.username,
            "password": self.password,
            "token": "token123"  # 假装是接口返回的toKen
        }
        r = requests.post(url, data=data)
        return r

if __name__ == '__main__':
    user_login = UserLogin("zhangsan", "mima123")
    token = user_login.get_token()
    print(token)
def dec():
    """
    python装饰器
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            func_name = func.__name__
            print(f"被装饰的方法名: {func_name}")
            print(f"方法的入参 args: {args}")
            print(f"方法的入参 kwargs: {kwargs}")

            r = func(*args, **kwargs)
            print(f"方法的返回值 return: {r}")

        return wrapper

    return decorator


@dec()
def add(a, b):
    c = a + b
    return c


add(1, 2)

# exceptions.py

class CustomException(Exception):
    """
    自定义异常类
    """

    def __init__(self, msg: str = None):
        self.msg = msg

    def __str__(self):
        exception_msg = f"Message: {self.msg}\n"
        return exception_msg


class AAError(CustomException):
    """
    AA type error
    """
    pass


class BBError(CustomException):
    """
    BB type error
    """
    pass


class CCError(CustomException):
    """
    CC type error
    """
    pass

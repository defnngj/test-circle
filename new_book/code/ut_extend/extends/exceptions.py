# exceptions.py

class CustomException(Exception):
    """
    自定义异常类
    """

    def __init__(self, msg: str = None, screen: str = None, stacktrace: str = None):
        self.msg = msg
        self.screen = screen
        self.stacktrace = stacktrace

    def __str__(self):
        exception_msg = f"Message: {self.msg}\n"
        if self.screen is not None:
            exception_msg += "Screenshot: available via screen\n"
        if self.stacktrace is not None:
            stacktrace = "\n".join(self.stacktrace)
            exception_msg += f"Stacktrace:\n{stacktrace}"
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

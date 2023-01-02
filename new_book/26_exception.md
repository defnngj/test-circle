
## 自定义异常

如果你要开发的是一个库或框架，那么自定义自己的错误类型有很多好处，比如可以清楚地显示出潜在的错误，让函数和模块更具可维护性。例如，我们在使用 selenium 的时候，经常看到这些异常：`NoSuchElementException`、`NoSuchAttributeException`等。通过这些异常，我们可以快速的将错误锁定到 selenium 的元素和 属性。


__功能代码__

在Python中实现自定义异常类。

```py
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

```

__代码说明__

CustomException 类继承 Exception 异常类。 msg 定义具体的异常信息。`AAError`、`BBError`、`CCError`根据需求定义不同的异常类。



__使用例子__

通过例子演示，在具体的场景中使用自定义异常类。

```py
from extends.exceptions import AAError


class_student = {"小红": 82, "小明": 99, "小刚": 73}


class Student:

    def __init__(self, name):
        self.name = name
        if name not in class_student.keys():
            raise AAError("`name` 不是班级学生.")

    def get_grade(self):
        return class_student[self.name]


if __name__ == '__main__':
    s = Student("小丽")
    grade = s.get_grade()
    print(grade)
```

__代码说明__

Student 类通过name 接收一个学生名字。如果学生名字不在 class_student中则抛出 `AAError` 异常。否则，可以调用 `get_grade()`方法 获得学生的成绩。


__运行结果__


```shell
> python test_exception.py

Traceback (most recent call last):
  File ".\test_exception.py", line 19, in <module>
    s = Student("小丽")
  File ".\test_exception.py", line 12, in __init__
    raise AAError("`name` 不是班级学生.")
extends.exceptions.AAError: Message: `name` 不是班级学生.
```

最后，我们需要理解异常和日志的区别，异常用于程序中断，也就是说，如果没有按照预设范围传参，程序将中断执行，而日志更多的是提供打印信息，帮助你了解程序的运行过程。

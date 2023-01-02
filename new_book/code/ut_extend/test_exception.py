# test_exception.py
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

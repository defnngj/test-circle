import unittest
from time import sleep
from concurrent.futures import ThreadPoolExecutor
from XTestRunner import HTMLTestRunner


class Test(unittest.TestCase):
    def test_case1(self):
        print("test_case1")
        sleep(3)

    def test_case2(self):
        print("test_case2")
        sleep(4)

    def test_case3(self):
        print("test_case3")
        sleep(5)


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(Test('test_case1'))
    suite.addTest(Test('test_case2'))
    suite.addTest(Test('test_case3'))
    res = unittest.TestResult()

    with ThreadPoolExecutor(max_workers=3) as executor:
        for s in suite:
            executor.submit(s.run, result=res)
    print("b", res)

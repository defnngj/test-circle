import unittest
from time import time, sleep
import threading
from concurrent.futures import ThreadPoolExecutor


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


def run_test(suites, thread_count=1):
    """
    多线程执行用例的方法
    :param suites: list -->包含多个套件的列表[TestSuite,TestSuite]
    :param thread_count: int  ---->执行的线程数量，默认为1
    :return: TestResult--->测试结果
    """
    res = unittest.TestResult()
    # 创建一个线程池，执行测试用例
    with ThreadPoolExecutor(max_workers=thread_count) as executor:
        for suite in suites:
            # 将套件的执行提交到线程池中
            executor.submit(suite.run, result=res)
    return res


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(Test('test_case1'))
    suite.addTest(Test('test_case2'))
    suite.addTest(Test('test_case3'))
    start_time = time()
    threads = []
    for i in range(3):
        t = threading.Thread(target=suite.run)
        threads.append(t)

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    end_time = time()
    print(f"run time: {start_time - end_time}")

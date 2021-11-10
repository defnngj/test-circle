import unittest
import os
from TestRunner import HTMLTestRunner
from tomorrow3 import threads

# 定义目录
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
TEST_DIR = os.path.join(BASE_DIR, "test_dir")
REPORT_DIR = os.path.join(BASE_DIR, "test_report")


def test_suits():
    """
    加载所有的测试用例
    """
    discover = unittest.defaultTestLoader.discover(
        TEST_DIR,
        pattern="test_*.py"
    )
    return discover


@threads(2)  # !!!核心!!!! 设置线程数
def run_case(all_case, nth=0):
    """
    执行所有的用例, 并把结果写入测试报告
    """
    report_abspath = os.path.join(REPORT_DIR, f"result{nth}.html")
    with open(report_abspath, "wb+") as file:
        runner = HTMLTestRunner(stream=file, title='多线程测试报告')
        # 调用test_suits函数返回值
        runner.run(all_case)


if __name__ == "__main__":
    cases = test_suits()
    # 循环启动线程
    for i, j in zip(cases, range(len(list(cases)))):
        run_case(i, nth=j)  # 执行用例，生成报告

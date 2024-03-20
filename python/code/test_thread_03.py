import unittest
from unittestreport import TestRunner

# 1、加载测试用例到套件中
suite = unittest.defaultTestLoader.discover(r'C:\project\open_class\Py0507\testcase')
runner = TestRunner(suite=suite)

# 2、设置5个线程去执行用例
runner.run(thread_count=5)



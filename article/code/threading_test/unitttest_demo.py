from time import sleep
import threading
import unittest

def raise_err():
    raise Exception()
def no_err():
    return

class Runner():

    def __init__(self):
        self.threads = {}
        self.thread_results = {}

    def add(self, target, name):
        self.threads[name] = threading.Thread(target = self.run, args = [target, name])
        self.threads[name].start()

    def run(self, target, name):
        self.thread_results[name] = 'fail'
        target()
        self.thread_results[name] = 'pass'

    def check_result(self, name):
        self.threads[name].join()
        assert(self.thread_results[name] == 'pass')

runner = Runner()

class MyTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        runner.add(no_err, 'test_raise_err')
        runner.add(no_err, 'test_no_err')
        runner.add(no_err, "test_case1")

    def test_raise_err(self):
        sleep(2)
        runner.check_result('test_raise_err')

    def test_no_err(self):
        sleep(3)
        runner.check_result('test_no_err')

    def test_case1(self):
        sleep(5)
        print("case1")


if __name__ == '__main__':
    unittest.main()
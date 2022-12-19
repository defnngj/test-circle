# test_jsonrunner.py
import unittest
from jsonrunner.runner import JSONTestRunner


class TestDemo(unittest.TestCase):
    """Test Demo class"""

    def test_pass(self):
        """pass case"""
        self.assertEqual(5, 5)

    @unittest.skip("skip case")
    def test_skip(self):
        """skip case"""
        ...

    def test_fail(self):
        """fail case"""
        self.assertEqual(5, 6)

    def test_error(self):
        """error case"""
        self.assertEqual(a, 6)


class TestDemo2(unittest.TestCase):
    """Test Demo2 class"""

    def test_pass(self):
        """pass case"""
        self.assertEqual(1+1, 2)

    def test_fail(self):
        """fail case"""
        self.assertEqual(5, 6)


if __name__ == '__main__':
    suit = unittest.TestSuite()
    suit.addTests([
        TestDemo("test_pass"),
        TestDemo("test_skip"),
        TestDemo("test_fail"),
        TestDemo("test_error"),
        TestDemo2("test_pass"),
        TestDemo2("test_fail")
    ])

    runner = JSONTestRunner(output="./result.json")
    runner.run(suit)
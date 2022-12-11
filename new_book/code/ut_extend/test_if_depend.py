# test_if_depend.py
import unittest
from extends.depend_extend import if_depend

class TestIfDepend(unittest.TestCase):
    depend_resule = True

    def test_001(self):
        TestIfDepend.depend_resule = False  # 修改depend_resule为 False

    @if_depend("depend_resule")
    def test_002(self):
        ...


if __name__ == '__main__':
    unittest.main()

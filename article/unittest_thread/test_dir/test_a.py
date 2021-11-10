import time
import unittest
from selenium import webdriver


class Test1(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()

    def test_01(self):
        self.driver.get("http://www.baidu.com")
        elem = self.driver.find_element_by_id("kw")
        elem.send_keys("unittest")
        elem.submit()
        time.sleep(2)
        self.assertEqual(self.driver.title, "unittest_百度搜索")

    def test_02(self):
        self.driver.get("http://www.baidu.com")
        elem = self.driver.find_element_by_id("kw")
        elem.send_keys("python")
        elem.submit()
        time.sleep(2)
        self.assertEqual(self.driver.title, "python_百度搜索")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()

import time
import unittest
from selenium import webdriver


class Test1(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()

    def test_01(self):
        self.driver.get("https://www.bing.com/?mkt=zh-CN")
        elem = self.driver.find_element_by_id("sb_form_q")
        elem.send_keys("多线程")
        elem.submit()
        time.sleep(2)
        self.assertIn("多线程", self.driver.title)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()

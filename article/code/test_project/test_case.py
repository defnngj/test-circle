import pytest
import yagmail
from selenium import webdriver


class MyTest:

    def setup(self):
        self.browser = webdriver.Chrome()

    def test_case(self):
        browser.find_element_by_id("user").send_keys("admin")
        browser.find_element_by_id("pawd").send_keys("admin123")
        # ...
        page.close()


if __name__ == "__main__":
    pytest.main(["-s", "-v", "./test_case.py",
        "--html", "./test_report.html",
        "--reruns", "3"
    ])
    yagmail.SMTP()
    # ...

import pytest
from common import mail
from test_data import TestData
from page import LoginPage


class MyTest:

    def test_case(self, browser):
        page = LoginPage(browser)
        page.username.send_keys(TestData.admin)
        page.passowrd.send_keys(TestData.admin_pawd)
        # ...
        page.close()


if __name__ == "__main__":
    pytest.main(["-s", "-v", "./test_case.py",
        "--html", "./test_report.html",
        "--reruns", "3"
    ])
    mail.SMTP()
    # ...

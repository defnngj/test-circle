import xtest
from xtest import TestData
from page import LoginPage


class MyTest(xtest.TestCase):

    def test_case(self):
        page = LoginPage(self.browser)
        page.username.send_keys(TestData.user)
        page.passowrd.send_keys(TestData.pawd)
        # ...

if __name__ == "__main__":
    xtest.main(mail=True)

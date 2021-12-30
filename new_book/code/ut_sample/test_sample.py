import xtest


class MyTest(xtest.TestCase):

    def test_case(self):
        self.say_hello(self.get_name, 3)


if __name__ == '__main__':
    xtest.run()

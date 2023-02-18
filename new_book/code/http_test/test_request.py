from common.case import TestCase, main


class MyHttpTest(TestCase):

    def test_get(self):
        payload = {'key1': 'value1', 'key2': 'value2'}
        r = self.get('https://httpbin.org/get', params=payload)
        self.assertEqual(r.status_code, 200)


if __name__ == '__main__':
    main()

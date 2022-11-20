import unittest
from extend.parameterized_extend import data
from extend.data_conversion import json_to_list, yaml_to_list, csv_to_list, excel_to_list
from extend.data_conversion import file_data

# @unittest.skip("七天无理由跳过")
# class ParamTestCase(unittest.TestCase):
#
#     @data([
#         ("2 and 3", 2, 3, 5),
#         ("10 and 20", 10, 20, 30),
#         ("hello and word", "hello", "world", "helloworld"),
#     ])
#     def test_add(self, _, a, b, expected):
#         self.assertEqual(a + b, expected)
#
#     @data([
#         {"scene": "username_is_null", "username": "", "password": "123"},
#         {"scene": "password_is_null", "username": "user", "password": ""},
#         {"scene": "login_success", "username": "user", "password": "123"},
#     ])
#     def test_login(self, name, username, password):
#         print(f"case: {name}, username: '{username}' password: '{password}'")
#

# class FileParamTestCase(unittest.TestCase):

    # @data(json_to_list("data/json_to_list_data.json", key="login"))
    # def test_login_json(self, name, username, password):
    #     print(f"case: {name}, username: '{username}' password: '{password}'")

    # @data(yaml_to_list("data/yaml_to_list_data.yaml", key="login"))
    # def test_login_yaml(self, name, username, password):
    #     print(f"case: {name}, username: '{username}' password: '{password}'")

    # @data(csv_to_list("data/csv_to_list_data.csv", line=2))
    # def test_login_csv(self, name, username, password):
    #     print(f"case: {name}, username: '{username}' password: '{password}'")

    # @data(excel_to_list("data/excel_to_list_data.xlsx", sheet="Sheet1", line=2))
    # def test_login_excel(self, name, username, password):
    #     print(f"case: {name}, username: '{username}' password: '{password}'")


class FileDataTestCase(unittest.TestCase):

    @file_data("data/json_to_list_data.json", key="login")
    def test_login_json(self, name, username, password):
        print(f"case: {name}, username: '{username}' password: '{password}'")

    @file_data("data/yaml_to_list_data.yaml", key="login")
    def test_login_yaml(self, name, username, password):
        print(f"case: {name}, username: '{username}' password: '{password}'")

    @file_data("data/csv_to_list_data.csv", line=2)
    def test_login_csv(self, name, username, password):
        print(f"case: {name}, username: '{username}' password: '{password}'")

    @file_data("data/excel_to_list_data.xlsx", sheet="Sheet1", line=2)
    def test_login_excel(self, name, username, password):
        print(f"case: {name}, username: '{username}' password: '{password}'")


if __name__ == '__main__':
    unittest.main(verbosity=1)


from running.runner import main
from running.loader_extend import MyTestLoader


if __name__ == '__main__':
    # # 开启收集用例开关
    # MyTestLoader.collectCaseInfo = True
    # # 指定运行用例目录
    # test_main = main(path="./test_dir/")
    # # 收集用用例
    # case_info = test_main.collect_cases(json=True)
    # print(case_info)

    # 收集到的用例列表
    cases = [
      {
        "file": "sub_dir.test_sub_case",
        "class": {
          "name": "TestSubDirCase",
          "doc": "子目录测试类"
        },
        "method": {
          "name": "test_sub_case",
          "doc": "test sub dir case"
        }
      }
    ]
    # 指定运行用例目录
    test_main = main(path="./test_dir")
    # 运行收集的用列
    test_main.run_cases(cases)

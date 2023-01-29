# argp.py
import argparse

# 1. 定义命令行解析器对象
parser = argparse.ArgumentParser(description='argparse 简单用法')

# 2. 添加命令行参数
parser.add_argument('-n', '--name', type=str, default="tom", help="请输入name名字，默认 tom")
parser.add_argument('-c', '--count', type=int, default=1, help="请输入次数，默认1")

# 3. 从命令行中结构化解析参数
args = parser.parse_args()

# 4. 使用参数
name = args.name
count = args.count
for _ in range(count):
    print(f"hello, {name}")
